import pytest
from ariadne.graphql import GraphQLError

from django.contrib.auth import get_user_model

from apps.graphql.resolvers.generics import (
    change_object_status,
    object_delete,
    object_edit,
)
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.investor import Investor, InvestorVersion

# noinspection PyProtectedMember
from ..resolvers.investor import _clean_payload

User = get_user_model()

payload: dict[str, any] = {
    # "investors": [],
    "name": "Sinnwerkstatt GmbH",
    "classification": "NON_PROFIT",
    "homepage": "sinnwerkstatt.com",
}


@pytest.fixture()
def investor_draft(db) -> list[int]:
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
    investor_id, investor_version = investor_draft

    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="reporter-2"),
            obj_id=investor_id,
            obj_version_id=investor_version,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investor_id).count() == 1

    object_delete(
        otype="investor",
        user=User.objects.get(username="reporter"),
        obj_id=investor_id,
        obj_version_id=investor_version,
        comment="weg mit dem schmutz",
    )
    assert Investor.objects.filter(id=investor_id).count() == 0


@pytest.fixture()
def test_edit_investor_draft(investor_draft):
    """
    :return: active investor
    """
    investor_id, investor_version = investor_draft

    land_reporter = User.objects.get(username="reporter")
    land_editor = User.objects.get(username="editor")
    land_admin = User.objects.get(username="administrator")

    # verify new draft
    i1 = Investor.objects.get(id=investor_id)
    assert i1.country_id == 276
    assert i1.draft_status == 1
    assert i1.status == 1
    i1v = i1.versions.get()
    assert i1v.serialized_data["draft_status"] == 1
    assert i1v.serialized_data["country"] == 276

    # edit draft
    pl2 = dict(payload, homepage="https://sinnwerkstatt.com")

    new_investor_id, new_investor_version = object_edit(
        otype="investor",
        user=User.objects.get(username="reporter"),
        obj_id=i1.id,
        obj_version_id=i1.versions.get().id,
        payload=pl2,
    )
    assert investor_id == new_investor_id
    assert investor_version == new_investor_version
    i1.refresh_from_db()
    assert i1.homepage == "https://sinnwerkstatt.com"

    i1v = i1.versions.get()
    assert i1v.serialized_data["homepage"] == "https://sinnwerkstatt.com"

    # change draft status TO_REVIEW
    investor_id, investor_version = change_object_status(
        otype="investor",
        user=land_reporter,
        obj_id=investor_id,
        obj_version_id=investor_version,
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
            obj_id=investor_id,
            obj_version_id=investor_version,
            transition="TO_ACTIVATION",
        )
    change_object_status(
        otype="investor",
        user=land_editor,
        obj_id=investor_id,
        obj_version_id=investor_version,
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
            obj_id=investor_id,
            obj_version_id=investor_version,
            transition="ACTIVATE",
        )
    change_object_status(
        otype="investor",
        user=land_admin,
        obj_id=investor_id,
        obj_version_id=investor_version,
        transition="ACTIVATE",
    )

    i1.refresh_from_db()
    assert i1.status == 2
    assert i1.draft_status is None

    return i1.id


def test_delete_investor(test_edit_investor_draft):
    investor_id = test_edit_investor_draft
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="reporter"),
            obj_id=investor_id,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investor_id).count() == 1
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="editor"),
            obj_id=investor_id,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investor_id).count() == 1
    object_delete(
        otype="investor",
        user=User.objects.get(username="administrator"),
        obj_id=investor_id,
        comment="weg mit dem schmutz",
    )
    i1 = Investor.objects.get()
    assert i1.status == STATUS["DELETED"]
    assert i1.draft_status is None


def test_edit_investor(test_edit_investor_draft):
    land_reporter = User.objects.get(username="reporter")
    i1 = Investor.objects.get()
    payload.update({"comment": "cool company"})
    investor_id, investor_version = object_edit(
        otype="investor",
        user=land_reporter,
        obj_id=i1.id,
        payload=payload,
    )
    assert investor_version is not None
    assert investor_id == i1.id
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
    investor_id = test_edit_investor_draft
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
    pl = _clean_payload(pl1, investor_id)

    inv_id, inv_v = object_edit(
        "investor", land_reporter, obj_id=investor_id, payload=pl
    )
    assert inv_id == investor_id

    i1 = Investor.objects.get(id=investor_id)
    assert i1.versions.count() == 2
    assert i1.investors.all().count() == 0

    i1v: InvestorVersion = i1.versions.first()  # newest version
    assert i1v.id == inv_v
    invs = i1v.serialized_data["investors"]  # involvements in version
    assert [(i["venture"], i["investor"]) for i in invs] == [(i1.id, i2.id)]
    assert invs[0]["id"] is None  # involvement should not have id yet.

    change_object_status("investor", land_admin, inv_id, inv_v, "TO_REVIEW")
    change_object_status("investor", land_admin, inv_id, inv_v, "TO_ACTIVATION")
    change_object_status("investor", land_admin, inv_id, inv_v, "ACTIVATE")

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
    pl = _clean_payload(pl1, investor_id)

    inv_id, inv_v2 = object_edit(
        "investor", land_reporter, obj_id=investor_id, payload=pl
    )

    change_object_status("investor", land_admin, inv_id, inv_v2, "TO_REVIEW")
    change_object_status("investor", land_admin, inv_id, inv_v2, "TO_ACTIVATION")
    change_object_status("investor", land_admin, inv_id, inv_v2, "ACTIVATE")
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
    pl = _clean_payload(pl1, investor_id)
    inv_id, inv_v3 = object_edit("investor", land_reporter, obj_id=i1.id, payload=pl)
    assert inv_v3 >= inv_v2
    change_object_status("investor", land_admin, inv_id, inv_v3, "TO_REVIEW")
    change_object_status("investor", land_admin, inv_id, inv_v3, "TO_ACTIVATION")
    change_object_status("investor", land_admin, inv_id, inv_v3, "ACTIVATE")
    i1.refresh_from_db()
    invs = i1.versions.all().first().serialized_data["investors"]
    assert [(i["venture"], i["investor"]) for i in invs] == [(i1.id, i3.id)]

    invos = i1.investors.all()
    assert [(i.venture_id, i.investor_id) for i in invos] == [
        (i1.id, i3.id),
    ]
