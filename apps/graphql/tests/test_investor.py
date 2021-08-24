from typing import List, Dict

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql import GraphQLError

from apps.graphql.resolvers.generics import (
    object_edit,
    change_object_status,
    object_delete,
)
from apps.landmatrix.models import Investor, InvestorVersion
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS

User = get_user_model()

payload: Dict[str, any] = {
    "investors": [],
    "name": "Sinnwerkstatt GmbH",
    "country": {"id": 276},
    "classification": "NON_PROFIT",
    "homepage": "sinnwerkstatt.com",
}


@pytest.fixture()
def investor_draft(db) -> List[int]:
    # new draft
    return object_edit(
        otype="investor",
        user=(User.objects.get(username="land_reporter")),
        obj_id=-1,
        obj_version_id=None,
        payload=payload,
    )


def test_delete_investor_draft(investor_draft):
    investorId, investorVersion = investor_draft

    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="land_reporter2"),
            obj_id=investorId,
            obj_version_id=investorVersion,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1

    object_delete(
        otype="investor",
        user=User.objects.get(username="land_reporter"),
        obj_id=investorId,
        obj_version_id=investorVersion,
        comment="weg mit dem schmutz",
    )
    assert Investor.objects.filter(id=investorId).count() == 0


@pytest.fixture()
def test_edit_investor_draft(investor_draft):
    investorId, investorVersion = investor_draft

    land_reporter = User.objects.get(username="land_reporter")
    land_editor = User.objects.get(username="land_editor")
    land_admin = User.objects.get(username="land_admin")

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
        user=User.objects.get(username="land_reporter"),
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
    print(i1)
    assert i1.status == 2
    assert i1.draft_status is None

    return i1.id


def test_delete_investor(test_edit_investor_draft):
    investorId = test_edit_investor_draft
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="land_reporter"),
            obj_id=investorId,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1
    with pytest.raises(GraphQLError):
        object_delete(
            otype="investor",
            user=User.objects.get(username="land_editor"),
            obj_id=investorId,
            comment="weg mit dem schmutz",
        )
    assert Investor.objects.filter(id=investorId).count() == 1
    object_delete(
        otype="investor",
        user=User.objects.get(username="land_admin"),
        obj_id=investorId,
        comment="weg mit dem schmutz",
    )
    i1 = Investor.objects.get()
    assert i1.status == STATUS["DELETED"]
    assert i1.draft_status is None


# noinspection PyUnusedLocal
def test_edit_investor(test_edit_investor_draft):
    land_reporter = User.objects.get(username="land_reporter")
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


# noinspection PyUnusedLocal
def test_add_involvements(test_edit_investor_draft):
    land_reporter = User.objects.get(username="land_reporter")

    pl = dict(
        payload,
        investors=[
            {
                "role": "PARENT",
                "id": 8024965410194944,
                "investor": {"id": 1525, "name": "16 foreign companies"},
                "investment_type": ["EQUITY"],
                "percentage": 12,
            }
        ],
    )

    i1 = Investor.objects.get()
    object_edit(
        otype="investor",
        user=land_reporter,
        obj_id=i1.id,
        payload=pl,
    )
    i1v: InvestorVersion = i1.versions.first()
    assert i1v.serialized_data["investors"] == [33]
