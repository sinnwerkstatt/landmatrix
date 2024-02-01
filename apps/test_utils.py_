import pytest
from graphql import GraphQLError

from django.contrib.auth import get_user_model

from apps.graphql.resolvers.generics import object_edit
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal
from apps.utils import qs_values_to_dict

user_model = get_user_model()


def test_country_is_mandatory():
    admin = user_model.objects.get(username="administrator")

    with pytest.raises(GraphQLError, match="COUNTRY_IS_MANDATORY"):
        object_edit("deal", admin, -1)


def test_related_resolver():
    reporter = user_model.objects.get(username="reporter")
    editor = user_model.objects.get(username="editor")

    albania = Country.objects.get(name="Albania")
    (obj_id, vers_id_1) = object_edit(
        "deal",
        reporter,
        -1,
        None,
        {"country": albania},
    )
    (_, vers_id_2) = object_edit(
        "deal",
        editor,
        obj_id,
        None,
        {"intended_size": 1_000.0},
    )

    assert qs_values_to_dict(
        Deal.objects.all(),
        [
            "country",
            "versions__created_by",
        ],
        ["versions"],
    ) == [
        {
            "id": obj_id,
            "country": albania.id,
            "versions": [
                {"id": vers_id_2, "created_by": editor.id},  # latest version first
                {"id": vers_id_1, "created_by": reporter.id},
            ],
        }
    ]
