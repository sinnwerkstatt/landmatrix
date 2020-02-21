from django.forms import (
    BooleanField,
    CharField,
    ChoiceField,
    DecimalField,
    FloatField,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from django.test import TestCase

from apps.grid.fields import (
    FileFieldWithInitial,
    TitleField,
    YearBasedIntegerField,
    YearBasedMultipleChoiceIntegerField,
)
from apps.grid.forms.base_form import *
from apps.landmatrix.models import Country, HistoricalActivity


class FieldsDisplayFormMixinTestCase(TestCase):

    fixtures = ["countries_and_regions"]

    def setUp(self):
        self.mixin = FieldsDisplayFormMixin()
        choices = (("value1", "label1"), ("value2", "label2"))
        nested_choices = (
            ("value1", "label1", None),
            ("value2", "label2", (("value2.1", "label2.1"), ("value2.2", "label2.2"))),
        )
        self.base_fields = {
            "tg_title": TitleField(),
            "nested_multiple_choice_field": NestedMultipleChoiceField(
                choices=nested_choices
            ),
            "model_multiple_choice_field": ModelMultipleChoiceField(
                queryset=Country.objects.all()
            ),
            "model_choice_field": ModelChoiceField(queryset=Country.objects.all()),
            "choice_field": ChoiceField(choices=choices),
            "area_field": AreaField(),
            "multi_value_field": YearBasedIntegerField(),
            "file_field": FileFieldWithInitial(),
            "boolean_field": BooleanField(),
            "char_field": CharField(),
        }
        self.initial = {
            "tg_title": "Title",
            "nested_multiple_choice_field": ["value1", "value2.1"],
            "model_multiple_choice_field": ["104", "116"],
            "model_choice_field": "104",
            "choice_field": "value1",
            "area_field": '{"type":"MultiPolygon","coordinates":[[[[100.39024939321291,-84.99256181934545],[100.96173157476198,-84.99458605320528],[100.90757241033326,-85.02036131846661],[100.31534065984499,-85.02277461634935],[100.39024939321291,-84.99256181934545]]]]}',
            "multi_value_field": "1:2000:",
            "file_field": "value",
            "boolean_field": "True",
            "char_field": "value",
        }

    def test_get_fields_display(self):
        self.mixin.base_fields = self.base_fields
        self.mixin.initial = self.initial
        values = self.mixin.get_fields_display()
        values_dict = dict((d["name"], d) for d in values)
        display_keys = {
            "tg",
            "nested_multiple_choice_field",
            "model_multiple_choice_field",
            "model_choice_field",
            "choice_field",
            "area_field",
            "multi_value_field",
            "file_field",
            "boolean_field",
            "char_field",
        }
        self.assertEqual(display_keys, set(values_dict.keys()))
        self.assertEqual(
            "label1<br>label2.1",
            values_dict.get("nested_multiple_choice_field").get("value"),
        )
        self.assertEqual(
            "Cambodia<br>Myanmar",
            values_dict.get("model_multiple_choice_field").get("value"),
        )
        self.assertEqual("Myanmar", values_dict.get("model_choice_field").get("value"))
        self.assertEqual("label1", values_dict.get("choice_field").get("value"))
        value = {
            "srid": 4326,
            "serialized": '{ "type": "MultiPolygon", "coordinates": [ [ [ [ 100.390249393212912, -84.992561819345454 ], [ 100.961731574761984, -84.994586053205282 ], [ 100.907572410333259, -85.020361318466612 ], [ 100.315340659844992, -85.022774616349352 ], [ 100.390249393212912, -84.992561819345454 ] ] ] ] }',
        }
        self.assertEqual(value, values_dict.get("area_field").get("value"))
        self.assertEqual("[2000] 1", values_dict.get("multi_value_field").get("value"))
        self.assertEqual("value", values_dict.get("file_field").get("value"))
        self.assertEqual("Yes", values_dict.get("boolean_field").get("value"))
        self.assertEqual("value", values_dict.get("char_field").get("value"))

    def assert_equal_display_value(self, value, field_name, method=None):
        if not method:
            method = f"get_display_value_{field_name}"
        self.mixin.base_fields = {field_name: self.base_fields.get(field_name)}
        self.mixin.initial = {field_name: self.initial.get(field_name)}
        display_value = getattr(self.mixin, method)(
            self.base_fields.get(field_name), field_name
        )
        self.assertEqual(value, display_value)

    def test_get_display_value_boolean_field(self):
        self.assert_equal_display_value("Yes", "boolean_field")
        self.initial["boolean_field"] = "False"
        self.assert_equal_display_value("No", "boolean_field")

    def test_get_display_value_file_field(self):
        self.assert_equal_display_value("value", "file_field")

    def test_get_display_value_multi_value_field(self):
        # 3 values (default)
        self.assert_equal_display_value("[2000] 1", "multi_value_field")
        # 4 values (e.g. crops with area, date and is_current)
        self.initial["multi_value_field"] = "1:3000:2000:"
        self.assert_equal_display_value("[2000] 1 (3000 ha)", "multi_value_field")
        # 2 values (invalid)
        self.initial["multi_value_field"] = "1:"
        self.assert_equal_display_value("", "multi_value_field")

    def test_get_display_value_choice_field(self):
        self.assert_equal_display_value("label1", "choice_field")

    def test_get_display_value_area_field(self):
        value = {
            "srid": 4326,
            "serialized": '{ "type": "MultiPolygon", "coordinates": [ [ [ [ 100.390249393212912, -84.992561819345454 ], [ 100.961731574761984, -84.994586053205282 ], [ 100.907572410333259, -85.020361318466612 ], [ 100.315340659844992, -85.022774616349352 ], [ 100.390249393212912, -84.992561819345454 ] ] ] ] }',
        }
        self.assert_equal_display_value(value, "area_field")

    def test_get_display_value_multiple_choice_field(self):
        self.assert_equal_display_value(
            "Cambodia<br>Myanmar",
            "model_multiple_choice_field",
            method="get_display_value_multiple_choice_field",
        )

    def test_get_display_value_nested_multiple_choice_field(self):
        self.assert_equal_display_value(
            "label1<br>label2.1", "nested_multiple_choice_field"
        )

    def test_get_display_value_model_choice_field(self):
        self.assert_equal_display_value("Myanmar", "model_choice_field")

        # Invalid pk
        self.initial = {"model_choice_field": "999a"}
        self.assert_equal_display_value("", "model_choice_field")

    def test_get_display_properties(self):
        mixin = FieldsDisplayFormMixin
        mixin.base_fields = self.base_fields
        doc = self.initial
        doc["multi_value_field_attr"] = [
            {"value": "value1", "date": "2000", "is_current": True},
            {"value": "value2", "date": "2010", "is_current": False},
        ]
        values_dict = FieldsDisplayFormMixin.get_display_properties(doc)
        display_keys = {
            "model_choice_field_display",
            "nested_multiple_choice_field_display",
            "boolean_field_display",
            "model_multiple_choice_field_display",
            "choice_field_display",
            "multi_value_field_display",
        }
        self.assertEqual(display_keys, set(values_dict.keys()))
        self.assertEqual(
            "label1|label2.1", values_dict.get("nested_multiple_choice_field_display")
        )
        self.assertEqual(
            "Myanmar|Cambodia", values_dict.get("model_multiple_choice_field_display")
        )
        self.assertEqual("Myanmar", values_dict.get("model_choice_field_display"))
        self.assertEqual("label1", values_dict.get("choice_field_display"))
        self.assertEqual(
            "2000#current#value1|2010##value2",
            values_dict.get("multi_value_field_display"),
        )
        self.assertEqual("Yes", values_dict.get("boolean_field_display"))


class BaseFormTestCase(TestCase):

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def setUp(self):
        self.form = BaseForm

        choices = (("value1", "label1"), ("value2", "label2"))
        nested_choices = (
            ("value1", "label1", None),
            ("value2", "label2", (("value2.1", "label2.1"), ("value2.2", "label2.2"))),
        )
        self.fields = {
            "tg_title": TitleField(),
            "nested_multiple_choice_field": NestedMultipleChoiceField(
                choices=nested_choices
            ),
            "model_multiple_choice_field": ModelMultipleChoiceField(
                queryset=Country.objects.all()
            ),
            "model_choice_field": ModelChoiceField(queryset=Country.objects.all()),
            "choice_field": ChoiceField(choices=choices),
            "multi_value_field_2": ActorsField(choices=choices),
            "multi_value_field_3a": YearBasedIntegerField(),
            "multi_value_field_3b": YearBasedIntegerField(),
            "multi_value_field_4": YearBasedMultipleChoiceIntegerField(choices=choices),
            "file_field": FileFieldWithInitial(),
            "decimal_field": DecimalField(),
            "float_field": FloatField(),
            "float_field_int": FloatField(),
            "char_field": CharField(),
        }
        self.data = MultiValueDict(
            {
                "nested_multiple_choice_field": [
                    "value1",
                    "value2.1",
                    "label2.1",
                    "invalid",
                ],  # test key, value and invalid
                "model_multiple_choice_field": ["104", "116"],
                "model_choice_field": ["104"],
                "choice_field": ["value1"],
                "multi_value_field_2_0": ["test"],
                "multi_value_field_2_1": ["value1"],
                "multi_value_field_3a_0": ["1"],
                "multi_value_field_3a_1": ["2000"],
                "multi_value_field_3a_2": ["on"],
                "multi_value_field_3b_0": ["1"],
                "multi_value_field_3b_1": ["2000"],
                # 'multi_value_field_3b_2': [''], - test incomplete values
                "multi_value_field_4_0": ["value1", "value2"],
                "multi_value_field_4_1": ["3000"],
                "multi_value_field_4_2": ["2000"],
                "multi_value_field_4_3": ["on"],
                "file_field": ["value"],
                "decimal_field": ["1.0"],
                "float_field": ["1.0"],
                "float_field_int": ["1"],  # test with integer
                "char_field": ["value"],
            }
        )
        self.attributes = {
            "nested_multiple_choice_field": [
                {"value": "label1"},
                {"value": "value2.1"},
                {"value": "label2.1"},
                {"value": "invalid"},
            ],
            "model_multiple_choice_field": [{"value": "104"}, {"value": "116"}],
            "model_choice_field": {"value": "104"},
            "choice_field": {"value": "label1"},
            "multi_value_field_2": [
                {"value": "test", "value2": "value1", "date": None, "is_current": False}
            ],
            "multi_value_field_3a": [
                {"value": "1", "value2": None, "date": "2000", "is_current": True}
            ],
            "multi_value_field_3b": [
                {"value": "1", "value2": None, "date": "2000", "is_current": False}
            ],
            "multi_value_field_4": [
                {
                    "value": "value1",
                    "value2": "3000",
                    "date": "2000",
                    "is_current": True,
                },
                {
                    "value": "value2",
                    "value2": "3000",
                    "date": "2000",
                    "is_current": True,
                },
            ],
            "file_field": {"value": "value"},
            "decimal_field": {"value": "1.0"},
            "float_field": {"value": "1.0"},
            "float_field_int": {"value": "1"},
            "char_field": {"value": "value"},
        }
        activity = HistoricalActivity.objects.create()
        for name, attribute in self.attributes.items():
            if not isinstance(attribute, (list, tuple)):
                attribute = [attribute]
            for attr in attribute:
                activity.attributes.create(name=name, **attr)
        self.activity = activity

    def test_get_attributes(self):
        self.form = self.form()
        self.form.fields = self.fields
        self.form.initial = self.data  # Necessary for file_field
        self.form.data = self.data
        attributes = self.form.get_attributes()
        attribute_keys = {
            "nested_multiple_choice_field",
            "model_multiple_choice_field",
            "model_choice_field",
            "choice_field",
            "multi_value_field_2",
            "multi_value_field_3a",
            "multi_value_field_3b",
            "multi_value_field_4",
            "file_field",
            "decimal_field",
            "float_field",
            "float_field_int",
            "char_field",
        }
        self.assertEqual(attribute_keys, set(attributes.keys()))
        self.assertEqual(
            [
                {"value": "label1"},
                {"value": "label2.1"},
                {"value": "label2.1"},
                {"value": "invalid"},
            ],
            attributes.get("nested_multiple_choice_field"),
        )
        self.assertEqual(
            [{"value": "104"}, {"value": "116"}],
            attributes.get("model_multiple_choice_field"),
        )
        self.assertEqual({"value": "104"}, attributes.get("model_choice_field"))
        self.assertEqual({"value": "label1"}, attributes.get("choice_field"))
        self.assertEqual(
            [{"value": "test", "value2": "value1", "date": None, "is_current": False}],
            attributes.get("multi_value_field_2"),
        )
        self.assertEqual(
            [{"value": "1", "value2": None, "date": "2000", "is_current": True}],
            attributes.get("multi_value_field_3a"),
        )
        self.assertEqual(
            [{"value": "1", "value2": None, "date": "2000", "is_current": False}],
            attributes.get("multi_value_field_3b"),
        )
        self.assertEqual(
            [
                {
                    "value": "value1",
                    "value2": "3000",
                    "date": "2000",
                    "is_current": True,
                },
                {
                    "value": "value2",
                    "value2": "3000",
                    "date": "2000",
                    "is_current": True,
                },
            ],
            attributes.get("multi_value_field_4"),
        )
        self.assertEqual({"value": "value"}, attributes.get("file_field"))
        self.assertEqual({"value": "1.0"}, attributes.get("decimal_field"))
        self.assertEqual({"value": "1.0"}, attributes.get("float_field"))
        self.assertEqual({"value": "1"}, attributes.get("float_field_int"))
        self.assertEqual({"value": "value"}, attributes.get("char_field"))

    def test_get_data(self):
        self.form.base_fields = self.fields
        data = self.form.get_data(self.activity)
        data_keys = {
            "nested_multiple_choice_field",
            "model_multiple_choice_field",
            "model_choice_field",
            "choice_field",
            "multi_value_field_2",
            "multi_value_field_3a",
            "multi_value_field_3b",
            "multi_value_field_4",
            "file_field",
            "decimal_field",
            "float_field",
            "float_field_int",
            "char_field",
        }
        self.assertEqual(data_keys, set(data.keys()))
        self.assertEqual(
            [["value1", "value2.1", "value2.1"]],
            data.getlist("nested_multiple_choice_field"),
        )
        self.assertEqual([["104", "116"]], data.getlist("model_multiple_choice_field"))
        self.assertEqual(["104"], data.getlist("model_choice_field"))
        self.assertEqual(["value1"], data.getlist("choice_field"))
        self.assertEqual(["test:value1"], data.getlist("multi_value_field_2"))
        self.assertEqual(["1:2000:1"], data.getlist("multi_value_field_3a"))
        self.assertEqual(["1:2000:"], data.getlist("multi_value_field_3b"))
        self.assertEqual(
            ["value1,value2:3000:2000:1"], data.getlist("multi_value_field_4")
        )
        self.assertEqual(["value"], data.getlist("file_field"))
        self.assertEqual(["1.0"], data.getlist("decimal_field"))
        self.assertEqual(["1.0"], data.getlist("float_field"))
        self.assertEqual(["1"], data.getlist("float_field_int"))
        self.assertEqual(["value"], data.getlist("char_field"))

    def assert_equal_field_value(self, value, field_name, method):
        self.form.base_fields = {field_name: self.fields.get(field_name)}
        field = self.fields.get(field_name)
        attributes = self.activity.attributes.filter(name=field_name)
        data = getattr(self.form, method)(field, field_name, attributes)
        if isinstance(value, (list, tuple)):
            self.assertEqual(set(value), set(data))
        else:
            self.assertEqual(value, data)

    def test_get_multiple_choice_data(self):
        self.assert_equal_field_value(
            ["116", "104"],
            field_name="model_multiple_choice_field",
            method="get_multiple_choice_data",
        )
        self.assert_equal_field_value(
            ["value2.1", "value2.1", "value1"],
            field_name="nested_multiple_choice_field",
            method="get_multiple_choice_data",
        )
        self.assert_equal_field_value(
            ["value1"], field_name="choice_field", method="get_multiple_choice_data"
        )

    def test_get_year_based_data(self):
        self.assert_equal_field_value(
            "1:2000:1", field_name="multi_value_field_3a", method="get_year_based_data"
        )
        self.assert_equal_field_value(
            "test:value1",
            field_name="multi_value_field_2",
            method="get_year_based_data",
        )

    def test_meta(self):
        self.form = self.form()
        self.assertEqual(self.form.Meta, self.form.meta)

    def test_init_with_exclude(self):
        self.form.base_fields = self.fields
        self.form.Meta.exclude = ("char_field",)
        self.form = self.form()
        self.assertNotIn("char_field", self.form.fields.keys())

    def test_init_with_fields(self):
        self.form.base_fields = self.fields
        self.form.Meta.fields = ("char_field",)
        self.form.Meta.readonly_fields = ()
        self.form = self.form()
        self.assertEqual({"char_field"}, set(self.form.fields.keys()))

    def test_init_with_readonly_fields(self):
        self.form.base_fields = self.fields
        self.form.Meta.readonly_fields = ("choice_field", "char_field")
        self.form = self.form()
        self.assertEqual(
            "disabled", self.form.fields.get("choice_field").widget.attrs["disabled"]
        )
        self.assertEqual(
            True, self.form.fields.get("char_field").widget.attrs["readonly"]
        )

    def tearDown(self):
        self.form.base_fields = {}
        self.form.Meta.exclude = ()
        self.form.Meta.fields = ()
        self.form.Meta.readonly_fields = ()
