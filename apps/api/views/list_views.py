import collections
import json
from copy import deepcopy

import coreapi
import coreschema
from django.contrib.auth import get_user_model
from django.http import Http404
from django.urls import reverse
from geojson import Feature, FeatureCollection, Point
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from apps.api.filters import (
    Filter,
    PresetFilter,
    get_list_element_by_key,
    remove_all_dict_keys_from_mixed_dict,
)
from apps.api.serializers import UserSerializer
from apps.api.utils import PropertyCounter
from apps.grid.forms.choices import INTENTION_AGRICULTURE_MAP, INTENTION_FORESTRY_MAP
from apps.grid.views.filter import FilterWidgetMixin
from apps.landmatrix.models import Country
from apps.landmatrix.models.activity import ActivityBase
from apps.landmatrix.models.investor import InvestorBase
from apps.map.views import MapSettingsMixin

User = get_user_model()

INTENTION_EXCLUDE = list(INTENTION_AGRICULTURE_MAP.keys())
INTENTION_EXCLUDE.extend(list(INTENTION_FORESTRY_MAP.keys()))


class ElasticSearchMixin:

    doc_type = "deal"
    request = None

    # default status are the public ones. will only get replaced if well formed and allowed
    status_list = ActivityBase.PUBLIC_STATUSES

    def get_filter_doc_type(self):
        """
        Returns doc type for filtering
        :return:
        """
        if self.doc_type == "location":
            return "deal"
        return self.doc_type

    def load_filters_from_url(self, exclude=[]):
        """
        Read any querystring param filters. Preset filters not allowed.
        """
        if self.request:
            variables = self.request.GET.getlist("variable")
            operators = self.request.GET.getlist("operator")
            values = self.request.GET.getlist("value")
        else:
            variables = []
            operators = []
            values = []
        combined = zip(variables, operators, values)

        filters = {
            f[0]: Filter(f[0], f[1], f[2]) for f in combined if f[0] not in exclude
        }

        return filters

    def load_filters(self, exclude=[]):
        filters = {}
        parent_company_filters, tertiary_investor_filters = {}, {}
        if self.request:
            session_filters = (
                self.request.session.get("%s:filters" % self.get_filter_doc_type(), {})
                or {}
            )
        else:
            session_filters = {}

        for filter_name, filter_dict in session_filters.items():
            if "preset_id" in filter_dict:
                filter = PresetFilter.from_session(filter_dict)
            else:
                filter = Filter.from_session(filter_dict)
                if filter["variable"] in exclude:
                    continue
            # FIXME: Make this work for filters presets too (no variable set)
            if "variable" in filter and filter["variable"].startswith(
                "parent_stakeholder_"
            ):
                filter["variable"] = filter["variable"].replace(
                    "parent_stakeholder_", ""
                )
                parent_company_filters[filter_name] = filter
            elif "variable" in filter and filter["variable"].startswith(
                "tertiary_investor_"
            ):
                filter["variable"] = filter["variable"].replace(
                    "tertiary_investor_", ""
                )
                tertiary_investor_filters[filter_name] = filter
            else:
                filters[filter_name] = filter
        # Create subquery for investor variable queries
        if parent_company_filters:
            query = {"bool": self.format_filters(parent_company_filters.values())}
            raw_result_list = self.execute_elasticsearch_query(query, "investor")
            operational_companies = []
            for result in raw_result_list:
                ids = result["_source"]["parent_company_of"]
                operational_companies.extend([str(id) for id in ids])
            filters["parent_company"] = self.get_investor_filter(operational_companies)
        if tertiary_investor_filters:
            query = {"bool": self.format_filters(tertiary_investor_filters.values())}
            raw_result_list = self.execute_elasticsearch_query(query, "investor")
            operational_companies = []
            for result in raw_result_list:
                ids = result["_source"]["tertiary_investor_of"]
                operational_companies.extend([str(id) for id in ids])
            filters["tertiary_investor"] = self.get_investor_filter(
                operational_companies
            )

        filters.update(self.load_filters_from_url(exclude=exclude))

        # note: passing only Filters, not (name, filter) dict!
        formatted_filters = self.format_filters(filters.values(), exclude=exclude)

        return formatted_filters

    def get_investor_filter(self, investors):
        return Filter(
            variable="operational_stakeholder", operator="in", value=investors
        )

    def format_filters(self, filters, initial_query=None, exclude=[]):
        """
        Generates an elasticsearch-conform `bool` query from session filters.
        This acts recursively for nested OR filter groups from preset filters
        @param filters: A list of Filter or PresetFilter
        @param query: (Optional) a dict resembling an elasticsearch bool query - filters will be
            added to this query instead of a new query. Use this for recursive calls.
        @return: a dict resembling an elasticsearch bool query, without the "{'bool': query}"
            wrapper
        """

        proto_filters = {
            "_filter_name": None,
            "must": [],  # AND
            "filter": [],  # EXCLUDE ALL OTHERS
            "must_not": [],  # AND NOT
            "should": [],  # OR
        }
        query = initial_query or deepcopy(proto_filters)

        # TODO: what about 'activity' or 'investor' filter type? (filter_obj.type)
        for filter_obj in filters:
            if isinstance(filter_obj, PresetFilter):
                # we here have multiple filters coming from a preset filter, add them recursively
                preset_filters = [
                    condition.to_filter()
                    for condition in filter_obj.filter.conditions.exclude(
                        variable__in=exclude
                    )
                ]
                if filter_obj.filter.relation == filter_obj.filter.RELATION_OR:
                    # for OR relations we build a new subquery that is ORed and add it to the must matches
                    preset_name = filter_obj.filter.name
                    # we are constructing a regular query, but because this is an OR order, we will take
                    # all the matches in the 'must' slot and add them to the 'should' list
                    filter_query = self.format_filters(preset_filters, exclude=exclude)
                    if filter_query.get("must", []) or filter_query.get("should", []):
                        conditions = filter_query.get("must", []) + filter_query.get(
                            "should", []
                        )
                        query["must"].append(
                            {
                                "bool": {
                                    "should": conditions,
                                    "minimum_should_match": 1,
                                },
                                "_filter_name": preset_name,
                            }
                        )
                    if filter_query.get("must_not", []):  # pragma: no cover
                        query["must_not"].append(
                            {
                                "bool": {
                                    "should": filter_query["must_not"],
                                    "minimum_should_match": 1,
                                },
                                "_filter_name": preset_name,
                            }
                        )
                else:
                    # for AND relations we just extend the filters into our current query
                    self.format_filters(
                        preset_filters, initial_query=query, exclude=exclude
                    )
            else:
                # add a single filter to our query

                # example: ('should', {'match': {'intention__value': 3},
                #                      '_filter_name': 'intention__value__not_in'})
                if filter_obj["variable"] in exclude:  # pragma: no cover
                    continue
                elastic_operator, elastic_match = filter_obj.to_elasticsearch_match()

                branch_list = query[elastic_operator]
                current_filter_name = elastic_match["_filter_name"]
                existing_match_phrase, existing_i = get_list_element_by_key(
                    branch_list, "_filter_name", current_filter_name
                )
                # if no filter exists for this yet, add it
                if existing_match_phrase is None:
                    branch_list.append(elastic_match)
                    # if elastic_operator == 'should':
                    #    query['minimum_should_match'] = 1
                else:
                    # if match phrase exists for this filter, and it is a bool,
                    # add the generated match(es) to its list
                    if "bool" in existing_match_phrase:  # pragma: no cover
                        if "must" in existing_match_phrase["bool"]:
                            existing_match_phrase["bool"]["must"].append(elastic_match)
                        else:
                            existing_match_phrase["bool"]["must"] = [elastic_match]
                    else:
                        # if match phrase exists and is a single match, pop it
                        existing_single_match = branch_list.pop(existing_i)
                        if "bool" in elastic_match:  # pragma: no cover
                            inside_operator = [
                                key_name
                                for key_name in elastic_match.keys()
                                if not key_name == "_filter_name"
                            ][0]
                            # if we have a bool, add the bool, add the popped match to bool
                            elastic_match[inside_operator].append(existing_single_match)
                            # if inside_operator == 'should':
                            #    elastic_match['minimum_should_match'] = 1
                            query["must"].append(elastic_match)
                        else:
                            # if  we have a single match, make new bool,
                            # add popped match and single match
                            matches = [existing_single_match, elastic_match]
                            query["must"].append(
                                {
                                    "bool": {elastic_operator: matches},
                                    "_filter_name": current_filter_name,
                                }
                            )
        # remove our meta attribute so the query is elaticsearch-conform
        if initial_query is None:
            remove_all_dict_keys_from_mixed_dict(query, "_filter_name")
        return query

    def create_query_from_filters(self, exclude=[]):
        # load filters from session
        query = self.load_filters(exclude=exclude)
        # add filters from request
        query = self.add_request_filters_to_elasticsearch_query(query, exclude=exclude)

        query = {"bool": query}
        return query

    def add_request_filters_to_elasticsearch_query(
        self, elasticsearch_query, exclude=[]
    ):
        window = None
        if self.request and self.request.GET.get("window", None):
            lon_min, lat_min, lon_max, lat_max = self.request.GET.get("window").split(
                ","
            )
            try:
                lat_min, lat_max = float(lat_min), float(lat_max)
                lon_min, lon_max = float(lon_min), float(lon_max)
                # respect the 180th meridian
                if lon_min > lon_max:  # pragma: no cover
                    lon_max, lon_min = lon_min, lon_max
                if lat_min > lat_max:  # pragma: no cover
                    lat_max, lat_min = lat_min, lat_max
                window = (lon_min, lat_min, lon_max, lat_max)
            except ValueError:  # pragma: no cover
                pass

        # add geo_point window match:
        if window:
            elasticsearch_query["filter"].append(
                {
                    "geo_bounding_box": {
                        "geo_point": {
                            "top_left": {
                                "lat": float(window[3]),
                                "lon": float(window[0]),
                            },
                            "bottom_right": {
                                "lat": float(window[1]),
                                "lon": float(window[2]),
                            },
                        }
                    }
                }
            )

        elasticsearch_query = self.add_status_logic(elasticsearch_query)
        elasticsearch_query = self.add_public_logic(elasticsearch_query)

        # TODO: these were at some point in the UI. add the missing filters!
        if self.request:
            request_filters = {
                "deal_scope": self.request.GET.getlist(
                    "deal_scope", ["domestic", "transnational"]
                ),
                "limit": self.request.GET.get("limit"),
                "investor_country": self.request.GET.get("investor_country"),
                "investor_region": self.request.GET.get("investor_region"),
                "target_country": self.request.GET.get("target_country"),
                "target_region": self.request.GET.get("target_region"),
                "attributes": self.request.GET.getlist("attributes", []),
            }
        else:
            request_filters = {
                "deal_scope": ["domestic", "transnational"],
                "limit": "",
                "investor_country": "",
                "investor_region": "",
                "target_country": "",
                "target_region": "",
                "attributes": [],
            }

        return elasticsearch_query

    def add_status_logic(self, query):
        # collect a proper and authorized-for-that-user status list from the requet paramert
        request_status_list = (
            self.request.GET.getlist("status", []) if self.request else []
        )
        if request_status_list and (
            self.request.user.is_superuser
            or self.request.user.has_perm("landmatrix.review_historicalactivity")
        ):
            status_list_get = [
                int(status)
                for status in request_status_list
                if (
                    status.isnumeric()
                    and int(status) in dict(ActivityBase.STATUS_CHOICES).keys()
                )
            ]
            if status_list_get:
                self.status_list = status_list_get

        query["filter"].append({"terms": {"status": self.status_list}})
        return query

    def add_public_logic(self, query):
        # Public user?
        if not self.request or self.request.user.is_anonymous:
            query["filter"].append(
                {"bool": {"filter": {"term": {"is_public": "True"}}}}
            )
        return query

    def execute_elasticsearch_query(
        self, query, doc_type="deal", fallback=True, sort=[], aggs={}
    ):
        from apps.api.elasticsearch import es_search

        es_search.refresh_index()
        # print('Elasticsearch query executed:\n')
        # from pprint import pprint
        # pprint(query)
        # pprint(aggs)

        try:
            results = es_search.search(query, doc_type=doc_type, sort=sort, aggs=aggs)
        except Exception as e:  # pragma: no cover
            raise
        return results

    def filter_deals(self, raw_result_list):
        """Additional filtering and exclusion of unwanted results"""
        result_list = []
        for raw_result in raw_result_list:
            result = raw_result["_source"]
            result["id"] = raw_result["_id"]
            result_list.append(result)

        # we have a special filter mode for status=STATUS_PENDING type searches,
        # if pending deals are to be shown, matched deals with status PENDING hide all other deals
        # with the same activity_identifier that are not PENDING
        if ActivityBase.STATUS_PENDING in self.status_list:
            pending_act_ids = [
                res["activity_identifier"]
                for res in result_list
                if res["status"] == ActivityBase.STATUS_PENDING
            ]
            for i in reversed(range(len(result_list))):
                res = result_list[i]
                if not res["status"] == ActivityBase.STATUS_PENDING:
                    activity_identifier = res["activity_identifier"]
                    # this match might be hidden if there is a pending match of PENDING status
                    if activity_identifier in pending_act_ids:
                        del result_list[i]

        return result_list

    def filter_investors(self, raw_result_list):
        """Additional filtering and exclusion of unwanted results"""
        result_list = []
        for raw_result in raw_result_list:
            result = raw_result["_source"]
            result["id"] = raw_result["_id"]
            result_list.append(result)

        # we have a special filter mode for status=STATUS_PENDING type searches,
        # if pending investors are to be shown, matched deals with status PENDING hide all other deals
        # with the same investor_identifier that are not PENDING
        if InvestorBase.STATUS_PENDING in self.status_list:
            pending_inv_ids = [
                res["investor_identifier"]
                for res in result_list
                if res["fk_status"] == InvestorBase.STATUS_PENDING
            ]
            for i in reversed(range(len(result_list))):
                res = result_list[i]
                if not res["fk_status"] == InvestorBase.STATUS_PENDING:
                    investor_identifier = res["investor_identifier"]
                    # this match might be hidden if there is a pending match of PENDING status
                    if investor_identifier in pending_inv_ids:
                        del result_list[i]

        return result_list

    def filter_involvements(self, raw_result_list, investors):
        """Additional filtering and exclusion of unwanted results"""
        result_list = []
        investor_ids = [int(i["id"]) for i in investors]
        involvements = {}

        for raw_result in raw_result_list:
            result = raw_result["_source"]
            # Include only involvements for given investors
            if (
                result["fk_venture"] not in investor_ids
                or result["fk_investor"] not in investor_ids
            ):
                continue
            key = "%s-%s" % (result["fk_venture_name"], result["fk_investor_name"])
            result["id"] = raw_result["_id"]
            result_list.append(result)
            # Save highest ID of duplicates
            if key not in involvements or involvements[key] < result["id"]:
                involvements[key] = result["id"]

        # Remove duplicates (only use highest ID e.g. if there are pending or older versions)
        for i in reversed(range(len(result_list))):
            result = result_list[i]
            key = "%s-%s" % (result["fk_venture_name"], result["fk_investor_name"])
            if key in involvements and involvements[key] != result["id"]:
                del result_list[i]

        return result_list

    def disable_filters(self):
        """
        Disable current filters temporarily and set default filters
        :param request:
        :return:
        """
        # Backup
        self.request.session[
            "%s:disabled_filters" % self.doc_type
        ] = self.request.session.get("%s:filters" % self.doc_type)
        self.request.session[
            "%s:disabled_set_default_filters" % self.doc_type
        ] = self.request.session.get("%s:set_default_filters" % self.doc_type, None)
        self.request.session["%s:filters" % self.doc_type] = {}
        self.request.session["%s:set_default_filters" % self.doc_type] = True
        # FIXME: Move FilterWidgetMixin.set_default_filters to utils
        f = FilterWidgetMixin()
        f.request = self.request
        f.set_country_region_filter(self.request.GET.copy())
        f.set_default_filters(None, disabled_presets=[2])

    def enable_filters(self):
        """
        Restore filters after being disabled by disable_filters()
        :return:
        """
        # Restore original filters
        self.request.session["%s:filters" % self.doc_type] = self.request.session.get(
            "%s:disabled_filters" % self.doc_type
        )
        if (
            self.request.session["%s:disabled_set_default_filters" % self.doc_type]
            is not None
        ):
            self.request.session[
                "%s:set_default_filters" % self.doc_type
            ] = self.request.session["%s:disabled_set_default_filters" % self.doc_type]
        del self.request.session["%s:disabled_filters" % self.doc_type]
        del self.request.session["%s:disabled_set_default_filters" % self.doc_type]


class UserListView(ListAPIView):
    """
    The users list view is used by the impersonate user feature of the editor.
    """

    queryset = User.objects.filter(is_active=True).order_by("first_name")
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class StatisticsView(ElasticSearchMixin, APIView):
    """
    Get deal aggregations grouped by Negotiation status.
    Used by the CMS plugin „statistics“ for homepages and regional/national landing pages.
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "country",
                required=True,
                location="query",
                description="Country ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "region",
                required=False,
                location="query",
                description="Region ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "disable_filters",
                required=False,
                location="query",
                description="Set to 1 to disable default filters",
                schema=coreschema.Integer(),
            ),
        ]
    )

    def get(self, request):
        target_country = request.GET.get("country", False)
        target_region = request.GET.get("region", False)
        disable_filters = request.GET.get("disable_filters", "") == "1"

        if disable_filters:
            self.disable_filters()
        query = self.create_query_from_filters()
        if target_country:
            query["bool"]["filter"].append({"term": {"target_country": target_country}})
        if target_region:
            query["bool"]["filter"].append({"term": {"target_region": target_region}})

        # Order by is set in aggregation
        aggs = {
            "current_negotiation_status": {
                "terms": {"field": "current_negotiation_status", "size": 100},
                "aggs": {
                    "deal_count": {
                        "terms": {"field": "activity_identifier", "size": 10000}
                    },
                    "deal_size_sum": {"sum": {"field": "deal_size"}},
                },
            }
        }
        # Search deals
        results = self.execute_elasticsearch_query(
            query, doc_type="deal", fallback=False, aggs=aggs
        )
        results = results["current_negotiation_status"]["buckets"]
        results = [
            [
                r["key"],
                len(r["deal_count"]["buckets"]),
                int(r["deal_size_sum"]["value"]),
            ]
            for r in results
        ]
        if disable_filters:
            self.enable_filters()
        return Response(results)

    def add_public_logic(self, query):
        # Always apply public filter
        query["filter"].append({"bool": {"filter": {"term": {"is_public": "True"}}}})
        return query


class LatestChangesView(ElasticSearchMixin, APIView):
    """
    Lists recent changes to the database (add, change, delete or comment)
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "n",
                required=False,
                location="query",
                description="Number of changes",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "target_country",
                required=True,
                location="query",
                description="Target country ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "target_region",
                required=True,
                location="query",
                description="Target region ID",
                schema=coreschema.Integer(),
            ),
        ]
    )

    def get(self, request):
        target_country = request.GET.get("target_country", False)
        target_region = request.GET.get("target_region", False)
        n = int(request.GET.get("n", "20"))

        query = self.create_query_from_filters()
        if target_country:
            query["bool"]["filter"].append({"term": {"target_country": target_country}})
        if target_region:
            query["bool"]["filter"].append({"term": {"target_region": target_region}})

        # Search deals
        raw_results = self.execute_elasticsearch_query(
            query, doc_type="deal", fallback=False, sort={"history_date": "desc"}
        )
        results = []
        for raw_result in raw_results[:n]:
            result = raw_result["_source"]
            target_country = result["target_country_display"]
            if len(target_country) > 0:
                target_country = target_country[0]
            results.append(
                {
                    "action": "add" if result["status"] == 2 else "change",
                    "deal_id": result["activity_identifier"],
                    "change_date": result["history_date"],
                    "target_country": target_country,
                }
            )

        return Response(results)


class GlobalDealsView(ElasticSearchMixin, APIView):

    """
    Get all deals from elasticsearch index.
    Used within the map section.
    """

    doc_type = "location"

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "window",
                required=False,
                location="query",
                description="Longitude min/max and Latitude min/max (e.g. 0,0,0,0)  ",
                schema=coreschema.String(),
            )
        ]
    )

    def get(self, request, *args, **kwargs):
        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)

        # filter results
        result_list = self.filter_deals(raw_result_list)
        # parse results
        features = list(
            filter(
                None,
                [self.create_feature_from_result(result) for result in result_list],
            )
        )
        response = Response(FeatureCollection(features))
        return response

    def get_intentions(self, intentions):
        """
        Returns parent intention count for Agriculture/Forestry
        :param intentions:
        :return:
        """
        agriculture, forestry = False, False
        for key, value in INTENTION_AGRICULTURE_MAP.items():
            if key in intentions:
                agriculture = True
                break
        if agriculture:
            intentions.append("Agriculture")
            intentions = list(
                filter(lambda i: i not in INTENTION_AGRICULTURE_MAP.keys(), intentions)
            )
        for key, value in INTENTION_FORESTRY_MAP.items():
            if key in intentions:
                forestry = True
                break
        if forestry:
            intentions.append("Forestry")
            intentions = list(
                filter(lambda i: i not in INTENTION_FORESTRY_MAP.keys(), intentions)
            )
        return intentions

    def create_feature_from_result(self, result):
        """Create a GeoJSON-conform result."""

        intended_size = result.get("intended_size", None)
        intended_size = (
            intended_size and intended_size[0]
        )  # saved as an array currently?
        contract_size = result.get("contract_size", None)
        contract_size = (
            contract_size and contract_size[0]
        )  # saved as an array currently?
        production_size = result.get("production_size", None)
        production_size = (
            production_size and production_size[0]
        )  # saved as an array currently?
        investor = result.get("operational_stakeholder", None)
        investor = investor and investor[0]  # saved as an array currently?

        # Remove subcategories from intention
        intention = self.get_intentions(result.get("intention", []))

        try:
            geometry = (float(result["point_lon"]), float(result["point_lat"]))
        except ValueError:  # pragma: no cover
            return None
        return Feature(
            # Do not use ID for feature. Duplicate IDs lead to problems in
            # Openlayers.
            geometry=Point(geometry),
            properties={
                "url": reverse(
                    "deal_detail", kwargs={"deal_id": result["activity_identifier"]}
                ),
                "intention": intention,
                "implementation": result.get("implementation_status", "Unknown"),
                "intended_size": intended_size,
                "contract_size": contract_size,
                "production_size": production_size,
                "investor": investor,
                "identifier": result.get("activity_identifier"),
                "level_of_accuracy": result.get("level_of_accuracy", "Unknown"),
            },
        )


class CountryDealsView(GlobalDealsView, APIView):
    """
    Get all deals grouped by country.
    Used within the map section.
    """

    def get(self, request, *args, **kwargs):
        """
        Reuse methods from globaldealsview, but group results by country.
        """
        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)

        # filter results
        result_list = self.filter_deals(raw_result_list)

        target_countries = collections.defaultdict(PropertyCounter)

        for result in result_list:
            if result.get("target_country"):
                target_countries[str(result["target_country"])].increment(**result)

        filter_country = self.request.GET.get("country_id")
        country_ids = [filter_country] if filter_country else target_countries.keys()
        countries = self.get_countries(*country_ids)

        features = []
        for country in countries:
            properties = {
                "name": country.name,
                "deals": len(target_countries[str(country.id)].activity_identifiers),
                "url": country.get_absolute_url(),
                "centre_coordinates": [country.point_lon, country.point_lat],
            }
            properties.update(target_countries[str(country.id)].get_properties())
            properties["intention"] = self.get_intentions(properties.get("intention"))
            features.append(
                {
                    "type": "Feature",
                    "id": country.code_alpha3,
                    # 'geometry': json.loads(country.geom),
                    "properties": properties,
                }
            )

        return Response(FeatureCollection(features))

    def get_intentions(self, intentions):
        """
        Returns parent intention count for Agriculture/Forestry
        :param intentions:
        :return:
        """
        if not intentions:  # pragma: no cover
            return {}
        agriculture_count, forestry_count = 0, 0
        for key, value in INTENTION_AGRICULTURE_MAP.items():
            agriculture_count += intentions.pop(key, 0)
        if agriculture_count > 0:
            intentions["Agriculture"] = agriculture_count
        for key, value in INTENTION_FORESTRY_MAP.items():
            forestry_count += intentions.pop(key, 0)
        if forestry_count > 0:
            intentions["Forestry"] = forestry_count
        return intentions

    def get_countries(self, *ids):
        """
        Get countries with simplified geometry, to reduce size of response.
        """
        return Country.objects.defer("geom").filter(id__in=ids)


class CountryGeomView(APIView):
    """
    Get minimal geojson of requested country. This works for one country only
    due to response size but can probably be reduced with ST_dump / ST_union for
    multiple countries.
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "country_id",
                required=False,
                location="query",
                description="Country ID",
                schema=coreschema.Integer(),
                example="104",
            )
        ]
    )

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return Response(
            data={
                "type": "Feature",
                "geometry": json.loads(self.get_queryset().simple_geom),
            }
        )

    def get_queryset(self):
        try:
            return Country.objects.extra(
                select={"simple_geom": "ST_AsGeoJSON(ST_Simplify(geom, 0.01))"}
            ).get(id=self.request.GET.get("country_id"))
        except Country.DoesNotExist:
            raise Http404


class PolygonGeomView(GlobalDealsView, APIView):
    """
    Get a GeoJSON representation of polygons. The polygon field is provided
    through kwargs, only fields defined in the MapSettingsMixin are valid.
    Currently no filtering is in place, all polygons encountered are returned.
    If this becomes too big, spatial filtering needs to be implemented.
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "polygon_field",
                required=True,
                location="path",
                description="Polygon field (contract_area, intended_area, production_area)",
                schema=coreschema.String(),
            )
        ]
    )
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        polygon_field = kwargs.get("polygon_field")

        valid_polygon_fields = MapSettingsMixin.get_polygon_layers().keys()
        if polygon_field not in valid_polygon_fields:
            raise Http404

        # Reuse methods from GlobalDealsView

        # Get the basic query filter for Elasticsearch
        query = {}  # self.create_query_from_filters()

        # Filter all objects which have an existing polygon field
        # TODO: Is there a better place and way for this?
        query = {"exists": {"field": polygon_field}}

        raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)
        result_list = self.filter_deals(raw_result_list)

        features = []
        for result in result_list:
            feature = result.get(polygon_field)
            if not feature:  # pragma: no cover
                continue

            # Again, case sensitive: multipolygon in ES needs to be MultiPolygon
            # in GeoJSON.
            feature = json.loads(feature)
            feature["type"] = "MultiPolygon"
            features.append(feature)

        return Response(FeatureCollection(features))
