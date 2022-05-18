from typing import List, Dict

import pytest
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from apps.graphql.resolvers.generics import (
    object_edit,
    change_object_status,
    object_delete,
)
from apps.graphql.resolvers.investor import _clean_payload
from apps.landmatrix.models import Investor, InvestorVersion, Country
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS

User = get_user_model()

payload: Dict[str, any] = {
    # "investors": [],
    "name": "Sinnwerkstatt GmbH",
    "classification": "NON_PROFIT",
    "homepage": "sinnwerkstatt.com",
}


@pytest.fixture()
def investor_draft(db) -> List[int]:
    payload["country"] = Country.objects.get(id=276)
    # new draft
    return object_edit(
        otype="investor",
        user=(User.objects.get(username="reporter")),
        obj_id=-1,
        obj_version_id=None,
        payload=payload,
    )


def test_delete_investor_draft(investor_draft):
    investorId, investorVersion = investor_draft

    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="reporter-2"),
            obj_id=investorId,
            obj_version_id=investorVersion,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1

    object_delete(
        otype="investor",
        user=User.objects.get(username="reporter"),
        obj_id=investorId,
        obj_version_id=investorVersion,
        comment="weg mit dem schmutz",
    )
    assert Investor.objects.filter(id=investorId).count() == 0


@pytest.fixture()
def test_edit_investor_draft(investor_draft):
    """
    :return: active investor
    """
    investorId, investorVersion = investor_draft

    land_reporter = User.objects.get(username="reporter")
    land_editor = User.objects.get(username="editor")
    land_admin = User.objects.get(username="administrator")

    # verify new draft
    i1 = Investor.objects.get(id=investorId)
    assert i1.country_id == 276
    assert i1.draft_status == 1
    assert i1.status == 1
    i1v = i1.versions.get()
    assert i1v.serialized_data["draft_status"] == 1
    assert i1v.serialized_data["country"] == 276

    # edit draft
    pl2 = dict(payload, homepage="https://sinnwerkstatt.com")

    newInvestorId, newInvestorVersion = object_edit(
        otype="investor",
        user=User.objects.get(username="reporter"),
        obj_id=i1.id,
        obj_version_id=i1.versions.get().id,
        payload=pl2,
    )
    assert investorId == newInvestorId
    assert investorVersion == newInvestorVersion
    i1.refresh_from_db()
    assert i1.homepage == "https://sinnwerkstatt.com"

    i1v = i1.versions.get()
    assert i1v.serialized_data["homepage"] == "https://sinnwerkstatt.com"

    # change draft status TO_REVIEW
    investorId, investorVersion = change_object_status(
        otype="investor",
        user=land_reporter,
        obj_id=investorId,
        obj_version_id=investorVersion,
        transition="TO_REVIEW",
    )
    i1.refresh_from_db()
    assert i1.draft_status == DRAFT_STATUS["REVIEW"]
    assert i1.versions.get().serialized_data["draft_status"] == DRAFT_STATUS["REVIEW"]

    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="investor",
            user=land_reporter,
            obj_id=investorId,
            obj_version_id=investorVersion,
            transition="TO_ACTIVATION",
        )
    change_object_status(
        otype="investor",
        user=land_editor,
        obj_id=investorId,
        obj_version_id=investorVersion,
        transition="TO_ACTIVATION",
    )
    i1.refresh_from_db()

    assert i1.draft_status == DRAFT_STATUS["ACTIVATION"]
    assert (
        i1.versions.get().serialized_data["draft_status"] == DRAFT_STATUS["ACTIVATION"]
    )

    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="investor",
            user=land_editor,
            obj_id=investorId,
            obj_version_id=investorVersion,
            transition="ACTIVATE",
        )
    change_object_status(
        otype="investor",
        user=land_admin,
        obj_id=investorId,
        obj_version_id=investorVersion,
        transition="ACTIVATE",
    )

    i1.refresh_from_db()
    assert i1.status == 2
    assert i1.draft_status is None

    return i1.id


def test_delete_investor(test_edit_investor_draft):
    investorId = test_edit_investor_draft
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="reporter"),
            obj_id=investorId,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="editor"),
            obj_id=investorId,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1
    object_delete(
        otype="investor",
        user=User.objects.get(username="administrator"),
        obj_id=investorId,
        comment="weg mit dem schmutz",
    )
    i1 = Investor.objects.get()
    assert i1.status == STATUS["DELETED"]
    assert i1.draft_status is None


# noinspection PyUnusedLocal
def test_edit_investor(test_edit_investor_draft):
    land_reporter = User.objects.get(username="reporter")
    i1 = Investor.objects.get()
    payload.update({"comment": "cool company"})
    investorId, investorVersion = object_edit(
        otype="investor",
        user=land_reporter,
        obj_id=i1.id,
        payload=payload,
    )
    assert investorVersion is not None
    assert investorId == i1.id
    i1.refresh_from_db()
    assert i1.comment == ""
    assert i1.status == STATUS["LIVE"]
    assert i1.draft_status == DRAFT_STATUS["DRAFT"]
    assert i1.versions.count() == 2
    i1v: InvestorVersion = i1.versions.first()
    assert i1v.serialized_data["draft_status"] == DRAFT_STATUS["DRAFT"]
    assert i1v.serialized_data["status"] == STATUS["LIVE"]
    assert i1v.serialized_data["comment"] == "cool company"

    payload.update(
        {"opencorporates": "https://opencorporates.com/companies/de/F1103R_HRB134255"}
    )
    object_edit(
        otype="investor",
        user=land_reporter,
        obj_id=i1.id,
        obj_version_id=i1v.id,
        payload=payload,
    )
    i1.refresh_from_db()
    assert i1.comment == ""
    assert i1.opencorporates == ""
    assert i1.status == 2
    assert i1.draft_status == DRAFT_STATUS["DRAFT"]
    assert i1.versions.count() == 2
    i1v.refresh_from_db()
    assert i1v.serialized_data["draft_status"] == DRAFT_STATUS["DRAFT"]
    assert i1v.serialized_data["status"] == STATUS["LIVE"]
    assert (
        i1v.serialized_data["opencorporates"]
        == "https://opencorporates.com/companies/de/F1103R_HRB134255"
    )


def test_add_involvements(test_edit_investor_draft):
    investorId = test_edit_investor_draft
    i2 = Investor.objects.create(name="Parent investor")
    i3 = Investor.objects.create(name="Parent investor2")

    land_reporter = User.objects.get(username="reporter")
    land_admin = User.objects.get(username="administrator")

    involvement1 = {
        "role": "PARENT",
        "investor": {"id": i2.id, "name": "Parent investor"},
        "investment_type": ["EQUITY"],
        "percentage": 12,
    }

    # this "dict" hack is here because of weird race conditions in pytest apparently
    pl1 = dict(payload, country={"id": "304"}, investors=[involvement1])
    pl = _clean_payload(pl1, investorId)

    invId, invV = object_edit("investor", land_reporter, obj_id=investorId, payload=pl)
    assert invId == investorId

    i1 = Investor.objects.get(id=investorId)
    assert i1.versions.count() == 2
    assert i1.investors.all().count() == 0

    i1v: InvestorVersion = i1.versions.first()  # newest version
    assert i1v.id == invV
    invs = i1v.serialized_data["investors"]  # involvements in version
    assert [(i["venture"], i["investor"]) for i in invs] == [(i1.id, i2.id)]
    assert invs[0]["id"] is None  # involvement should not have id yet.

    change_object_status("investor", land_admin, invId, invV, "TO_REVIEW")
    change_object_status("investor", land_admin, invId, invV, "TO_ACTIVATION")
    change_object_status("investor", land_admin, invId, invV, "ACTIVATE")

    invo1 = i1.investors.all()[0]
    assert invo1.id
    involvement1["id"] = invo1.id
    assert invo1.role == "PARENT"
    assert invo1.investment_type == ["EQUITY"]

    # add an investor
    involvement2 = {
        "role": "PARENT",
        "investor": {"id": i3.id},
        "investment_type": ["EQUITY"],
        "percentage": 23,
    }
    pl1 = dict(payload, country={"id": "304"}, investors=[involvement1, involvement2])
    pl = _clean_payload(pl1, investorId)

    invId, invV2 = object_edit("investor", land_reporter, obj_id=investorId, payload=pl)

    change_object_status("investor", land_admin, invId, invV2, "TO_REVIEW")
    change_object_status("investor", land_admin, invId, invV2, "TO_ACTIVATION")
    change_object_status("investor", land_admin, invId, invV2, "ACTIVATE")
    i1.refresh_from_db()
    invs = i1.versions.all().first().serialized_data["investors"]

    assert [(i["venture"], i["investor"]) for i in invs] == [
        (i1.id, i2.id),
        (i1.id, i3.id),
    ]
    invos = i1.investors.all()
    assert invs[0]["id"] == invos[1].id
    assert [(i.venture_id, i.investor_id) for i in invos] == [
        (i1.id, i3.id),
        (i1.id, i2.id),
    ]

    involvement2["id"] = invos[0].id
    assert involvement1["id"] == invos[1].id

    # remove an investor
    pl1 = dict(payload, country={"id": "304"}, investors=[involvement2])
    pl = _clean_payload(pl1, investorId)
    invId, invV3 = object_edit("investor", land_reporter, obj_id=i1.id, payload=pl)
    assert invV3 >= invV2
    change_object_status("investor", land_admin, invId, invV3, "TO_REVIEW")
    change_object_status("investor", land_admin, invId, invV3, "TO_ACTIVATION")
    change_object_status("investor", land_admin, invId, invV3, "ACTIVATE")
    i1.refresh_from_db()
    invs = i1.versions.all().first().serialized_data["investors"]
    assert [(i["venture"], i["investor"]) for i in invs] == [(i1.id, i3.id)]

    invos = i1.investors.all()
    assert [(i.venture_id, i.investor_id) for i in invos] == [
        (i1.id, i3.id),
    ]
