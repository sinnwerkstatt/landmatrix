from django.test import RequestFactory, TestCase

from apps.api.templatetags.filter_tags import *
from apps.landmatrix.models import Country, Region
from apps.wagtailcms.models import CountryPage, RegionPage


class FilterTagsTestCase(TestCase):

    fixtures = (
        'countries_and_regions',
    )

    def setUp(self):
        request = RequestFactory()
        request.GET = QueryDict(mutable=True)
        self.context = {
            'request': request,
        }

    def test_filter_query_params_with_params(self):
        context = self.context
        context['request'].GET['status'] = '1'
        params = filter_query_params(context)
        self.assertEqual('?status=1', params)

    def test_filter_query_params_without_params(self):
        params = filter_query_params(self.context)
        self.assertEqual('', params)

    def test_list_params_with_country(self):
        context = self.context
        context['country'] = Country.objects.get(id=104)
        params = list_params(context)
        self.assertEqual('?country=104', params)

    def test_list_params_with_region(self):
        context = self.context
        context['region'] = Region.objects.get(id=142)
        params = list_params(context)
        self.assertEqual('?region=142', params)

    def test_list_params_with_country_page(self):
        context = self.context
        context['page'] = CountryPage.objects.create(title='Myanmar Page', country_id=104,
                                                     path='/', depth=0)
        params = list_params(context)
        self.assertEqual('?country=104', params)

    def test_list_params_with_region_page(self):
        context = self.context
        context['page'] = RegionPage.objects.create(title='Asia Page', region_id=142,
                                                    path='/', depth=0)
        params = list_params(context)
        self.assertEqual('?region=142', params)

    def test_list_params_with_request_country(self):
        context = self.context
        context['request'].GET['country'] = 104
        params = list_params(context)
        self.assertEqual('?country=104', params)

    def test_list_params_with_request_region(self):
        context = self.context
        context['request'].GET['region'] = 142
        params = list_params(context)
        self.assertEqual('?region=142', params)

    def test_list_params_with_request_status(self):
        context = self.context
        context['request'].GET['status'] = 1
        params = list_params(context)
        self.assertEqual('?status=1', params)
