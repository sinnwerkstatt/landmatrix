from collections import OrderedDict

import coreapi
import coreschema
from django.utils.translation import ugettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from apps.api.serializers import RegionSerializer
from apps.landmatrix.models import Country
from apps.landmatrix.templatetags.landmatrix_tags import nav_countries
from apps.wagtailcms.models import CountryPage, RegionPage
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
        countries = nav_countries()
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

    # def get_serializer(self, page, many=False):
    #     return None

    def get_queryset(self):
        results = {}

        term = self.request.GET.get('q', '')
        if term:
            # latest_ids = HistoricalInvestor.objects.latest_ids()
            # queryset = HistoricalInvestor.objects.filter(id__in=latest_ids)
            # queryset = queryset.filter(name__icontains=term.lower())
            # results = []
            # for investor in queryset:
            #    top_investors = ""
            #    if "unknown" in investor.name.lower():
            #        top_investors = investor.format_investors(investor.get_top_investors())
            #    results.append({
            #        "id": investor.id,
            #        "text": investor.name,
            #        "investor_identifier": investor.investor_identifier,
            #        "country": str(investor.fk_country),
            #        "top_investors": top_investors,
            #    })
            query = {
                'bool': {
                    'must': [
                        {'bool': {
                            'should': [
                                {'match_phrase': {'name': term.lower()}},
                                {'wildcard': {'name': '*%s*' % term.lower()}},
                            ],
                            'minimum_should_match': 1
                        }},
                        {'terms': {'fk_status': [1, 2, 3]}},
                    ]
                }
            }
            # Search deals
            raw_results = self.execute_elasticsearch_query(query, doc_type='investor',
                                                           fallback=False,
                                                           sort='name.raw')
            results = OrderedDict()
            for raw_result in raw_results:
                result = raw_result['_source']
                id = result["investor_identifier"]
                if id in results:
                    # Always prefer pending version
                    if results[id]["fk_status"] == 1:  # pragma: no cover
                        continue
                results[id] = {
                    "id": raw_result["_id"],
                    "text": result["name"],
                    "investor_identifier": result["investor_identifier"],
                    "country": result["fk_country_display"],
                    "top_investors": result["top_investors"],
                    "fk_status": result["fk_status"],
                }

        return list(results.values())

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page) if page else Response(queryset)
