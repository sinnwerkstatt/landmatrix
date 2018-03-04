from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.schemas import ManualSchema
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi
import coreschema

from wagtailcms.models import RegionPage
from api.query_sets.countries_query_set import CountriesQuerySet
from api.serializers import RegionSerializer
from api.views.base import FakeQuerySetListView
from .list_views import ElasticSearchMixin


class CountryListView(FakeQuerySetListView):
    """
    Get all countries grouped by National Observatories and Others.
    Used by the navigation.
    """
    fake_queryset_class = CountriesQuerySet


class RegionListView(ListAPIView):
    """
    Get all regions.
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
                'wildcard': {'name': '*%s*' % term},
            }
            # Search deals
            raw_results = self.execute_elasticsearch_query(query, doc_type='investor',
                                                           fallback=False,
                                                           sort='name')
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

