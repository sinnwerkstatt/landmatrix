from django.test import RequestFactory, TestCase

from apps.wagtailcms.blocks import get_country_or_region_link, get_country_or_region
from apps.wagtailcms.wagtail_hooks import (
    editor_css,
    editor_js,
    whitelister_element_rules,
)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class WagtailCMSModelsTestCase(TestCase):
    fixtures = ["countries_and_regions"]

    def test_get_country_or_region_with_request_country(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={"country_slug": "myanmar"})
        result = get_country_or_region(request)
        self.assertEqual(104, result.get("country").id)

    def test_get_country_or_region_with_request_region(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={"region_slug": "asia"})
        result = get_country_or_region(request)
        self.assertEqual(142, result.get("region").id)

    def test_get_country_or_region_link_with_country(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={"country_slug": "myanmar"})
        link = get_country_or_region_link("url", request=request)
        self.assertEqual("url?country=104", link)

    def test_get_country_or_region_link_with_region(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={"region_slug": "asia"})
        link = get_country_or_region_link("url", request=request)
        self.assertEqual("url?region=142", link)

    def test_editor_js(self):
        self.assertGreater(len(editor_js()), 0)

    def test_editor_css(self):
        self.assertGreater(len(editor_css()), 0)

    def test_whitelister_element_rules(self):
        rules = whitelister_element_rules()
        self.assertIsInstance(rules, dict)
        self.assertGreater(len(rules.keys()), 0)
