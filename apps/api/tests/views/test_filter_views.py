from django.http import QueryDict
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.api.views.filter_views import *
from apps.landmatrix.models import FilterPreset


class FilterDocTypeMixinTestCase(TestCase):
    def test_dispatch(self):
        request = RequestFactory()
        request.method = "OPTIONS"
        request.path = "/"
        mixin = FilterDocTypeMixin()
        response = mixin.dispatch(request, doc_type="investor")
        self.assertEqual("investor", mixin.doc_type)


class FilterCreateViewTestCase(TestCase):

    fixtures = ["filters"]

    def test_filter_with_deal(self):
        data = {"variable": "activity_identifier", "operator": "is", "value": "1"}
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        new_filter = list(stored_filters.values())[0]
        self.assertEqual("activity_identifier", new_filter.get("variable"))
        self.assertEqual("is", new_filter.get("operator"))
        self.assertEqual("1", new_filter.get("value"))
        self.assertEqual("Deal ID", new_filter.get("label"))

    def test_filter_with_investor(self):
        data = {"variable": "investor_identifier", "operator": "is", "value": "1"}
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "investor"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("investor:filters")
        new_filter = list(stored_filters.values())[0]
        self.assertEqual("investor_identifier", new_filter.get("variable"))
        self.assertEqual("is", new_filter.get("operator"))
        self.assertEqual("1", new_filter.get("value"))
        self.assertEqual("Investor ID", new_filter.get("label"))

    def test_filter_with_replace_variable(self):
        custom_filter = {
            "name": "custom_filter",
            "variable": "activity_identifier",
            "operator": "is",
            "value": "1",
            "label": "Deal ID",
            "key": None,
            "display_value": "1",
        }
        session = self.client.session
        session["deal:filters"] = {"custom_filter": custom_filter}
        session.save()

        data = {
            "variable": "activity_identifier",
            "operator": "is",
            "value": "2",
            "replace_variable": True,
        }
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        new_filter = list(stored_filters.values())[0]
        self.assertEqual("activity_identifier", new_filter.get("variable"))
        self.assertEqual("is", new_filter.get("operator"))
        self.assertEqual("2", new_filter.get("value"))
        self.assertEqual("Deal ID", new_filter.get("label"))

    def test_filter_with_duplicates(self):
        custom_filter = {
            "name": "custom_filter",
            "variable": "activity_identifier",
            "operator": "is",
            "value": "1",
            "label": "Deal ID",
            "key": None,
            "display_value": "1",
        }
        session = self.client.session
        session["deal:filters"] = {"custom_filter": custom_filter}
        session.save()

        data = {"variable": "activity_identifier", "operator": "is", "value": "1"}
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual(1, len(stored_filters.keys()))

    def test_preset_with_deal(self):
        data = {"preset": "1"}
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        new_preset = list(stored_filters.values())[0]
        self.assertEqual("1", new_preset.get("preset_id"))

    def test_preset_with_duplicates(self):
        custom_preset = {
            "name": "custom_preset",
            "preset_id": "1",
            "label": "Exclude Mining",
            "hidden": False,
        }
        session = self.client.session
        session["deal:filters"] = {"custom_preset": custom_preset}
        session.save()

        data = {"preset": "1"}
        response = self.client.post(
            reverse("api_filter_create", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual(1, len(stored_filters.keys()))


class FilterDeleteViewTestCase(TestCase):
    def setUp(self):
        custom_filter = {
            "name": "custom_filter",
            "variable": "activity_identifier",
            "operator": "is",
            "value": "1",
            "label": "Deal ID",
            "key": None,
            "display_value": "1",
        }
        session = self.client.session
        session["deal:filters"] = {"custom_filter": custom_filter}
        session.save()

    def test(self):
        data = {"name": "custom_filter"}
        response = self.client.post(
            reverse("api_filter_delete", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual({}, stored_filters)

    def test_with_invalid_name(self):
        data = {"name": "invalid_filter"}
        response = self.client.post(
            reverse("api_filter_delete", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual({"custom_filter"}, set(stored_filters.keys()))

    def test_without_name(self):
        data = {"name": ""}
        response = self.client.post(
            reverse("api_filter_delete", kwargs={"doc_type": "deal"}), data=data
        )
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual({"custom_filter"}, set(stored_filters.keys()))


class SetDefaultFiltersViewTestCase(TestCase):

    fixtures = ["filters"]

    def test(self):
        data = {"set_default_filters": "1"}
        response = self.client.post(
            reverse("api_filter_set_default_filters", kwargs={"doc_type": "deal"}),
            data=data,
        )
        set_default_filters = self.client.session.get("deal:set_default_filters")
        self.assertEqual(True, set_default_filters)

    def test_without_set_default_filters(self):
        data = {"set_default_filters": ""}
        response = self.client.post(
            reverse("api_filter_set_default_filters", kwargs={"doc_type": "deal"}),
            data=data,
        )
        set_default_filters = self.client.session.get("deal:set_default_filters")
        self.assertEqual(False, set_default_filters)


class FilterListViewTestCase(TestCase):
    def test(self):
        custom_filter = {
            "name": "custom_filter",
            "variable": "activity_identifier",
            "operator": "is",
            "value": "1",
            "label": "Deal ID",
            "key": None,
            "display_value": "1",
        }
        session = self.client.session
        session["deal:filters"] = {"custom_filter": custom_filter}
        session.save()
        response = self.client.get(
            reverse("api_filter_list", kwargs={"doc_type": "deal"})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual({"custom_filter": custom_filter}, response.data)


class FilterClearViewTestCase(TestCase):
    def test(self):
        custom_filter = {
            "name": "custom_filter",
            "variable": "activity_identifier",
            "operator": "is",
            "value": "1",
            "label": "Deal ID",
            "key": None,
            "display_value": "1",
        }
        session = self.client.session
        session["deal:filters"] = {"custom_filter": custom_filter}
        session.save()
        response = self.client.get(
            reverse("api_filter_clear", kwargs={"doc_type": "deal"})
        )
        stored_filters = self.client.session.get("deal:filters")
        self.assertEqual({}, stored_filters)


class FilterPresetViewTestCase(TestCase):

    fixtures = ["filters"]

    def test(self):
        response = self.client.get(
            reverse("api_filter_preset", kwargs={"doc_type": "deal"})
        )
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for preset in FilterPreset.objects.all():
            self.assertIn(preset.name, response_dict.keys())
            self.assertEqual(preset.id, response_dict[preset.name]["id"])
            self.assertEqual(preset.is_hidden, response_dict[preset.name]["is_hidden"])

    def test_with_group(self):
        data = QueryDict("group=1")
        response = self.client.get(
            reverse("api_filter_preset", kwargs={"doc_type": "deal"}), data
        )
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for preset in FilterPreset.objects.filter(group_id=1):
            self.assertIn(preset.name, response_dict.keys())
            self.assertEqual(preset.id, response_dict[preset.name]["id"])
            self.assertEqual(preset.is_hidden, response_dict[preset.name]["is_hidden"])

    def test_with_show_groups(self):
        data = QueryDict("show_groups=1")
        response = self.client.get(
            reverse("api_filter_preset", kwargs={"doc_type": "deal"}), data
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual({3, 5, 4, 2, 1}, set(response.data))
