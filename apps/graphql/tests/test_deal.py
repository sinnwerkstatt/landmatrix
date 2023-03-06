from typing import Type

import pytest
from ariadne.graphql import GraphQLError

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.accounts.models import User
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal, DealVersion

from ..resolvers.generics import change_object_status, object_delete, object_edit

UserModel: Type[User] = get_user_model()

payload: dict[str, any] = {
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
def deal_draft(db) -> list[int]:
    payload["country"] = Country.objects.get(id=450)
    # new draft
    return object_edit(
        otype="deal",
        user=(UserModel.objects.get(username="reporter")),
        obj_id=-1,
        obj_version_id=None,
        payload=payload,
    )


def test_delete_deal_draft(deal_draft):
    deal_id, deal_version = deal_draft

    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=UserModel.objects.get(username="reporter-2"),
            obj_id=deal_id,
            obj_version_id=deal_version,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=deal_id).count() == 1

    object_delete(
        otype="deal",
        user=UserModel.objects.get(username="reporter"),
        obj_id=deal_id,
        obj_version_id=deal_version,
        comment="weg mit dem schmutz",
    )
    assert Deal.objects.filter(id=deal_id).count() == 0


@pytest.fixture()
def test_edit_deal_draft(deal_draft):
    deal_id, deal_version = deal_draft

    # verify new draft
    d1 = Deal.objects.get(id=deal_id)
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
            "country": Country.objects.get(id=450),
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

    new_deal_id, new_deal_version = object_edit(
        otype="deal",
        user=UserModel.objects.get(username="reporter"),
        obj_id=d1.id,
        obj_version_id=d1.versions.get().id,
        payload=pl2,
    )
    assert deal_id == new_deal_id
    assert deal_version == new_deal_version
    d1.refresh_from_db()
    assert d1.locations[0]["description"] == ""
    assert d1.locations[0]["comment"] == "KOMMA"
    d1v = d1.versions.get()
    assert d1v.serialized_data["locations"][0]["description"] == ""
    assert d1v.serialized_data["locations"][0]["comment"] == "KOMMA"

    # change draft status TO_REVIEW
    deal_id, deal_version = change_object_status(
        otype="deal",
        user=UserModel.objects.get(username="reporter"),
        obj_id=deal_id,
        obj_version_id=deal_version,
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
            user=UserModel.objects.get(username="reporter"),
            obj_id=deal_id,
            obj_version_id=deal_version,
            transition="TO_ACTIVATION",
            fully_updated=True,
        )
    change_object_status(
        otype="deal",
        user=UserModel.objects.get(username="editor"),
        obj_id=deal_id,
        obj_version_id=deal_version,
        transition="TO_ACTIVATION",
        fully_updated=True,
    )
    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="deal",
            user=UserModel.objects.get(username="editor"),
            obj_id=deal_id,
            obj_version_id=deal_version,
            transition="ACTIVATE",
            fully_updated=True,
        )
    change_object_status(
        otype="deal",
        user=UserModel.objects.get(username="administrator"),
        obj_id=deal_id,
        obj_version_id=deal_version,
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
    deal_id = test_edit_deal_draft
    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=UserModel.objects.get(username="reporter"),
            obj_id=deal_id,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=deal_id).count() == 1
    with pytest.raises(GraphQLError):
        object_delete(
            otype="deal",
            user=UserModel.objects.get(username="editor"),
            obj_id=deal_id,
            comment="weg mit dem schmutz",
        )
    assert Deal.objects.filter(id=deal_id).count() == 1
    object_delete(
        otype="deal",
        user=UserModel.objects.get(username="administrator"),
        obj_id=deal_id,
        comment="weg mit dem schmutz",
    )
    d1 = Deal.objects.get()
    assert d1.status == STATUS["DELETED"]
    assert d1.draft_status is None


def test_edit_deal(test_edit_deal_draft):
    d1 = Deal.objects.get()
    payload.update({"intended_size": 1000})
    deal_id, deal_version = object_edit(
        otype="deal",
        user=UserModel.objects.get(username="reporter"),
        obj_id=d1.id,
        payload=payload,
    )
    assert deal_version is not None
    assert deal_id == d1.id
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
        user=UserModel.objects.get(username="reporter"),
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
