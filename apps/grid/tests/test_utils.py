from django.contrib.auth import get_user_model
from django.forms import BooleanField, CharField, ModelChoiceField

from apps.grid.fields import (
    ActorsField,
    AreaField,
    NestedMultipleChoiceField,
    YearBasedChoiceField,
    YearBasedMultipleChoiceIntegerField,
)
from apps.grid.tests.views.base import BaseDealTestCase
from apps.grid.utils import *
from apps.landmatrix.models import (
    Country,
    HistoricalActivity,
    HistoricalInvestor,
    ActivityChangeset,
)
from apps.landmatrix.tests.mixins import InvestorsFixtureMixin, ActivitiesFixtureMixin


class GridUtilsTestCase(
    ActivitiesFixtureMixin, InvestorsFixtureMixin, BaseDealTestCase
):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]
    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
    ]

    inv_fixtures = [{"id": 1, "investor_identifier": 1, "name": "Test Investor #1"}]

    def test_get_display_value_without_value(self):
        self.assertEqual("", get_display_value(CharField(), []))

    def test_get_display_value_with_investor_choice_field(self):
        field = ModelChoiceField(queryset=HistoricalInvestor.objects.all())
        self.assertEqual("1", get_display_value(field, ["1"]))

    def test_get_display_value_with_user_choice_field(self):
        field = ModelChoiceField(queryset=Country.objects.all())
        self.assertEqual("Myanmar", get_display_value(field, ["104"]))

    def test_get_display_value_with_nested_choice_field(self):
        choices = (
            ("value1", "label1", None),
            ("value2", "label2", (("value2.1", "label2.1"), ("value2.2", "label2.2"))),
        )
        field = NestedMultipleChoiceField(choices=choices)
        self.assertEqual(
            "label1|label2.1", get_display_value(field, ["value1", "value2.1"])
        )

    def test_get_display_value_with_area_field(self):
        self.assertEqual("", get_display_value(AreaField(), []))

    def test_get_display_value_with_year_based_choice_field(self):
        field = YearBasedChoiceField(
            choices=HistoricalActivity.NEGOTIATION_STATUS_CHOICES
        )
        attributes = [
            dict(
                name="negotiation_status",
                value="Expression of interest",
                value2="",
                date="1000",
                is_current=False,
            )
        ]
        self.assertEqual(
            "1000##Intended (Expression of interest)",
            get_display_value(field, "test", attributes=attributes),
        )

    def test_get_display_value_with_actors_fields(self):
        choices = (("value1", "label1"), ("value2", "label2"))
        field = ActorsField(choices=choices)
        attributes = [
            dict(
                name="actor",
                value="test1",
                value2="value1",
                date=None,
                is_current=False,
            ),
            dict(
                name="actor",
                value="test2",
                value2="value2",
                date=None,
                is_current=False,
            ),
        ]
        self.assertEqual(
            "test1#value1|test2#value2",
            get_display_value(field, "test", attributes=attributes),
        )

    def test_get_display_value_with_year_based_multiple_choice_integer_field(self):
        field = YearBasedMultipleChoiceIntegerField(
            choices=HistoricalActivity.NEGOTIATION_STATUS_CHOICES
        )
        attributes = [
            dict(
                name="intention",
                value="Mining",
                value2="1",
                date="1000",
                is_current=True,
            ),
            dict(
                name="intention",
                value="Timber plantation",
                value2="2",
                date="2000",
                is_current=False,
            ),
        ]
        self.assertEqual(
            "1000#current#1#Mining|2000##2#Timber plantation",
            get_display_value(field, "test", attributes=attributes),
        )

    def test_get_display_value_with_boolean_field(self):
        field = BooleanField()
        self.assertEqual("Yes", get_display_value(field, ["True"]))

    def test_get_display_value_with_formset(self):
        field = BooleanField()
        self.assertEqual(
            ["Yes", "No"], get_display_value(field, ["True", ""], formset=True)
        )

    def test_get_spatial_properties(self):
        keys = {
            "level_of_accuracy",
            "location",
            "point_lat",
            "point_lon",
            "facility_name",
            "target_country",
            "location_description",
            "contract_area",
            "intended_area",
            "production_area",
            "tg_location_comment",
        }
        self.assertEqual(keys, set(get_spatial_properties()))

    def test_has_perm_approve_reject_with_superuser(self):
        user = get_user_model().objects.get(username="superuser")
        self.assertEqual(True, has_perm_approve_reject(user))

    def test_has_perm_approve_reject_with_editor(self):
        user = get_user_model().objects.get(username="editor")
        activity = HistoricalActivity.objects.get(id=1)
        self.assertEqual(True, has_perm_approve_reject(user, object=activity))

    def test_has_perm_approve_reject_with_editor_reviewed(self):
        ActivityChangeset.objects.create(
            fk_activity_id=2, fk_user_id=3, comment="Test changeset"
        )
        user = get_user_model().objects.get(username="editor")
        activity = HistoricalActivity.objects.get(id=2)
        self.assertEqual(False, has_perm_approve_reject(user, object=activity))
