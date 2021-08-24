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
from apps.landmatrix.models import Deal, DealVersion
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS

User = get_user_model()

payload: Dict[str, any] = {
    "country": {"id": 450},
    "locations": [
        {
            "id": 1,
            "point": {"lat": -18.92566, "lng": 47.54364},
            "areas": {"type": "FeatureCollection", "features": []},
            "level_of_accuracy": "APPROXIMATE_LOCATION",
            "name": "Villa Berlin, Lalana Rainmanga Rahanamy, Antananarivo, Madagaskar",
            "description": "villa berlin :)",
        }
    ],
}


@pytest.fixture()
def deal_draft(db) -> List[int]:
    # new draft
    return object_edit(
        otype="deal",
        user=(User.objects.get(username="land_reporter")),
        obj_id=-1,
        obj_version_id=None,
        payload=payload,
    )


def test_delete_deal_draft(deal_draft):
    dealId, dealVersion = deal_draft

    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=User.objects.get(username="land_reporter2"),
            obj_id=dealId,
            obj_version_id=dealVersion,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=dealId).count() == 1

    object_delete(
        otype="deal",
        user=User.objects.get(username="land_reporter"),
        obj_id=dealId,
        obj_version_id=dealVersion,
        comment="weg mit dem schmutz",
    )
    assert Deal.objects.filter(id=dealId).count() == 0


@pytest.fixture()
def test_edit_deal_draft(deal_draft):
    dealId, dealVersion = deal_draft

    land_reporter = User.objects.get(username="land_reporter")
    land_editor = User.objects.get(username="land_editor")
    land_admin = User.objects.get(username="land_admin")

    # verify new draft
    d1 = Deal.objects.get(id=dealId)
    assert d1.country_id == 450
    print(d1)
    print(d1.locations)
    assert d1.locations[0]["description"] == "villa berlin :)"
    assert d1.draft_status == DRAFT_STATUS["DRAFT"]
    assert d1.status == STATUS["DRAFT"]
    d1v = d1.versions.get()
    assert d1v.serialized_data["draft_status"] == DRAFT_STATUS["DRAFT"]
    assert d1v.serialized_data["country"] == 450

    # edit draft
    pl2 = dict(
        payload,
        **{
            "country": {"id": 450},
            "locations": [
                {
                    "id": 1,
                    "name": "Villa Berlin, Lalana Rainmanga Rahanamy, Antananarivo, Madagaskar",
                    "areas": {"type": "FeatureCollection", "features": []},
                    "point": {"lat": -18.92566, "lng": 47.54364},
                    "description": "",
                    "level_of_accuracy": "APPROXIMATE_LOCATION",
                    "comment": "KOMMA",
                }
            ],
        },
    )

    newDealId, newDealVersion = object_edit(
        otype="deal",
        user=User.objects.get(username="land_reporter"),
        obj_id=d1.id,
        obj_version_id=d1.versions.get().id,
        payload=pl2,
    )
    assert dealId == newDealId
    assert dealVersion == newDealVersion
    d1.refresh_from_db()
    assert d1.locations[0]["description"] == ""
    assert d1.locations[0]["comment"] == "KOMMA"
    d1v = d1.versions.get()
    assert d1v.serialized_data["locations"][0]["description"] == ""
    assert d1v.serialized_data["locations"][0]["comment"] == "KOMMA"

    # change draft status TO_REVIEW
    dealId, dealVersion = change_object_status(
        otype="deal",
        user=land_reporter,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="TO_REVIEW",
        fully_updated=True,
    )
    d1.refresh_from_db()
    assert d1.draft_status == DRAFT_STATUS["REVIEW"]
    assert d1.versions.get().serialized_data["draft_status"] == DRAFT_STATUS["REVIEW"]

    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="deal",
            user=land_reporter,
            obj_id=dealId,
            obj_version_id=dealVersion,
            transition="TO_ACTIVATION",
            fully_updated=True,
        )
    change_object_status(
        otype="deal",
        user=land_editor,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="TO_ACTIVATION",
        fully_updated=True,
    )
    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="deal",
            user=land_editor,
            obj_id=dealId,
            obj_version_id=dealVersion,
            transition="ACTIVATE",
            fully_updated=True,
        )
    change_object_status(
        otype="deal",
        user=land_admin,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="ACTIVATE",
        fully_updated=True,
    )

    d1.refresh_from_db()
    assert d1.status == STATUS["LIVE"]
    assert d1.draft_status is None
    assert d1.fully_updated is True
    assert d1.fully_updated_at.date() == timezone.now().date()
    return d1.id


def test_delete_deal(test_edit_deal_draft):
    dealId = test_edit_deal_draft
    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=User.objects.get(username="land_reporter"),
            obj_id=dealId,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=dealId).count() == 1
    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=User.objects.get(username="land_editor"),
            obj_id=dealId,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=dealId).count() == 1
    object_delete(
        otype="deal",
        user=User.objects.get(username="land_admin"),
        obj_id=dealId,
        comment="weg mit dem schmutz",
    )
    d1 = Deal.objects.get()
    assert d1.status == STATUS["DELETED"]
    assert d1.draft_status is None


def test_edit_deal(test_edit_deal_draft):
    land_reporter = User.objects.get(username="land_reporter")
    d1 = Deal.objects.get()
    payload.update({"intended_size": 1000})
    dealId, dealVersion = object_edit(
        otype="deal",
        user=land_reporter,
        obj_id=d1.id,
        payload=payload,
    )
    assert dealVersion is not None
    assert dealId == d1.id
    d1.refresh_from_db()
    assert d1.intended_size is None
    assert d1.status == STATUS["LIVE"]
    assert d1.draft_status == DRAFT_STATUS["DRAFT"]
    assert d1.versions.count() == 2
    d1v: DealVersion = d1.versions.first()
    assert d1v.serialized_data["draft_status"] == DRAFT_STATUS["DRAFT"]
    assert d1v.serialized_data["status"] == STATUS["LIVE"]
    assert d1v.serialized_data["intended_size"] == 1000

    payload.update({"land_area_comment": "too large"})
    object_edit(
        otype="deal",
        user=land_reporter,
        obj_id=d1.id,
        obj_version_id=d1v.id,
        payload=payload,
    )
    d1.refresh_from_db()
    assert d1.intended_size is None
    assert d1.land_area_comment == ""
    assert d1.status == STATUS["LIVE"]
    assert d1.draft_status == DRAFT_STATUS["DRAFT"]
    assert d1.versions.count() == 2
    d1v.refresh_from_db()
    assert d1v.serialized_data["draft_status"] == DRAFT_STATUS["DRAFT"]
    assert d1v.serialized_data["status"] == STATUS["LIVE"]
    assert d1v.serialized_data["land_area_comment"] == "too large"
