from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.schemas import ManualSchema
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi
import coreschema

from api.serializers import RegionSerializer
from api.views.base import FakeQuerySetListView
from landmatrix.models import Country
from wagtailcms.models import CountryPage, RegionPage
from .list_views import ElasticSearchMixin


class CountryListView(APIView):
    """
    Get all countries.
    """
    def get(self, request):
        queryset = Country.objects.all()
        queryset = queryset.only('id', 'slug', 'name').order_by('name')
        response = [[c.id, c.slug, c.name] for c in queryset]
        return Response(response)


class TargetCountryListView(APIView):
    """
    Get all target countries grouped by National Observatories and Others.
    Used by the navigation.
    """
    def get(self, request):
        countries = []
        observatories = CountryPage.objects.filter(live=True).order_by('title')
        countries.append({
            'text': _('Observatories'),
            'children': [
                [country.country.id if country.country else None, country.slug, country.title]
                for country in observatories]
        })
        other_countries = Country.objects.filter(is_target_country=True, high_income=False)
        other_countries = other_countries.exclude(id__in=[c.country.id
                                                          for c in observatories if c.country])
        other_countries = other_countries.only('id', 'slug', 'name').order_by('name')
        countries.append({
            'text': _('Other'),
            'children': [[country.id, country.slug, country.name] for country in other_countries]
        })
        return Response(countries)


class RegionListView(ListAPIView):
    """
    Get all target regions.
    Used by the navigation.
    """
    # Filter out pages without an assigned region, those just error
    queryset = RegionPage.objects.filter(
        region__isnull=False).order_by('title')
    serializer_class = RegionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class InvestorListView(ElasticSearchMixin,
                       ListAPIView):
    """
    Get all Operating companies, Parent companies and Tertiary investors/lenders.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "q",
                required=False,
                location="query",
                description="Search term",
                schema=coreschema.String(),
            ),
        ]
    )
    pagination_class = StandardResultsSetPagination

    def get_serializer(self, page, many=False):
        return None

    def get_queryset(self):
        results = []

        term = self.request.GET.get('q', '')
        if term:
            query = {
                'bool': {
                    'must': [
                        {'wildcard': {'name.raw': '*%s*' % term.lower()}},
                        {'terms': {'fk_status': [2, 3]}},
                    ]
                }
            }
            # Search deals
            raw_results = self.execute_elasticsearch_query(query, doc_type='investor',
                                                           fallback=False,
                                                           sort='name.raw')
            results = []
            for raw_result in raw_results:
                result = raw_result['_source']
                results.append({
                    "id": raw_result["_id"],
                    "text": result["name"],
                    "investor_identifier": result["investor_identifier"],
                    "country": result["fk_country_display"],
                    "top_investors": result["top_investors"],
                })

        return results

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(queryset)

