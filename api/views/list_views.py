import json
import collections
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

from api.utils import PropertyCounter
from api.serializers import UserSerializer
from landmatrix.models import Country
from landmatrix.models.activity import ActivityBase
from geojson import FeatureCollection, Feature, Point
from grid.forms.choices import INTENTION_AGRICULTURE_MAP, INTENTION_FORESTRY_MAP
from map.views import MapSettingsMixin
from api.filters import Filter, PresetFilter, remove_all_dict_keys_from_mixed_dict, \
    get_list_element_by_key
from grid.views.filter_widget_mixin import FilterWidgetMixin

User = get_user_model()

INTENTION_EXCLUDE = list(INTENTION_AGRICULTURE_MAP.keys())
INTENTION_EXCLUDE.extend(list(INTENTION_FORESTRY_MAP.keys()))


class ElasticSearchMixin(object):

    doc_type = 'deal'
    request = None

    # default status are the public ones. will only get replaced if well formed and allowed
    status_list = ActivityBase.PUBLIC_STATUSES

    def load_filters_from_url(self):
        '''
        Read any querystring param filters. Preset filters not allowed.
        '''
        if self.request:
            variables = self.request.GET.getlist('variable')
            operators = self.request.GET.getlist('operator')
            values = self.request.GET.getlist('value')
        else:
            variables = []
            operators = []
            values = []
        combined = zip(variables, operators, values)

        filters = {f[0]: Filter(f[0], f[1], f[2]) for f in combined}

        return filters

    def load_filters(self):
        filters = {}
        parent_company_filters, tertiary_investor_filters = {}, {}
        if self.request:
            session_filters = self.request.session.get('filters', {}) or {}
        else:
            session_filters = {}

        for filter_name, filter_dict in session_filters.items():
            if 'preset_id' in filter_dict:
                filter = PresetFilter.from_session(filter_dict)
            else:
                filter = Filter.from_session(filter_dict)
            # FIXME: Make this work for filters presets too (no variable set)
            if 'variable' in filter and filter['variable'].startswith('parent_stakeholder_'):
                filter['variable'] = filter['variable'].replace('parent_stakeholder_', '')
                parent_company_filters[filter_name] = filter
                filter['variable'] = filter['variable'].replace('tertiary_investor_', '')
            elif 'variable' in filter and filter['variable'].startswith('tertiary_investor_'):
                tertiary_investor_filters[filter_name] = filter
            else:
                filters[filter_name] = filter
        # Create subquery for investor variable queries
        if parent_company_filters:
            query = {'bool': self.format_filters(parent_company_filters.values())}
            raw_result_list = self.execute_elasticsearch_query(query, 'investor')
            operational_companies = []
            for result in raw_result_list:
                ids = result['_source']['parent_company_of']
                operational_companies.extend([str(id) for id in ids])
            filters['parent_company'] = Filter(variable='operational_stakeholder',
                operator='in', value=operational_companies)
        if tertiary_investor_filters:
            query = self.format_filters(tertiary_investor_filters.values())
            raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)
            operational_companies = []
            for result in raw_result_list:
                ids = result['_source']['tertiary_investor_of']
                operational_companies.extend([str(id) for id in ids])
            filters['tertiary_investor'] = Filter(variable='operational_stakeholder',
                operator='in', value=operational_companies)

        filters.update(self.load_filters_from_url())

        # note: passing only Filters, not (name, filter) dict!
        formatted_filters = self.format_filters(filters.values())


        return formatted_filters

    def format_filters(self, filters, initial_query=None):
        """
            Generates an elasticsearch-conform `bool` query from session filters.
            This acts recursively for nested OR filter groups from preset filters
            @param filters: A list of Filter or PresetFilter
            @param query: (Optional) a dict resembling an elasticsearch bool query - filters will be
                added to this query instead of a new query. Use this for recursive calls.
            @return: a dict resembling an elasticsearch bool query, without the "{'bool': query}"
                wrapper
        """
        from api.elasticsearch import get_elasticsearch_properties

        proto_filters = {
            '_filter_name': None,
            'must': [],  # AND
            'filter': [],  # EXCLUDE ALL OTHERS
            'must_not': [],  # AND NOT
            'should': [],  # OR
        }
        query = initial_query or deepcopy(proto_filters)

        # TODO: what about 'activity' or 'investor' filter type? (filter_obj.type)
        for filter_obj in filters:
            if isinstance(filter_obj, PresetFilter):
                # we here have multiple filters coming from a preset filter, add them recursively
                preset_filters = [condition.to_filter() for condition in
                                  filter_obj.filter.conditions.all()]
                if filter_obj.filter.relation == filter_obj.filter.RELATION_OR:
                    # for OR relations we build a new subquery that is ORed and add it to the must matches
                    preset_name = filter_obj.filter.name
                    # we are constructing a regular query, but because this is an OR order, we will take
                    # all the matches in the 'must' slot and add them to the 'should' list
                    filter_query = self.format_filters(preset_filters)
                    if filter_query.get('must', None) or filter_query.get('should', ''):
                        query['must'].append({
                            'bool': {
                                'should': filter_query['must'] + filter_query['should']
                            },
                            '_filter_name': preset_name
                        })
                    if filter_query.get('must_not', None):
                        query['must_not'].append({
                            'bool': {
                                'should': filter_query['must_not']
                            },
                            '_filter_name': preset_name
                        })
                else:
                    # for AND relations we just extend the filters into our current query
                    self.format_filters(preset_filters, initial_query=query)
            else:
                # add a single filter to our query

                # example: ('should', {'match': {'intention__value': 3},
                #                      '_filter_name': 'intention__value__not_in'})
                elastic_operator, elastic_match = filter_obj.to_elasticsearch_match()

                branch_list = query[elastic_operator]
                current_filter_name = elastic_match['_filter_name']
                existing_match_phrase, existing_i = get_list_element_by_key(branch_list,
                                                                            '_filter_name',
                                                                            current_filter_name)
                # if no filter exists for this yet, add it
                if existing_match_phrase is None:
                    branch_list.append(elastic_match)
                else:
                    # if match phrase exists for this filter, and it is a bool,
                    # add the generated match(es) to its list
                    if 'bool' in existing_match_phrase:
                        inside_operator = [key_name for key_name in existing_match_phrase.keys()
                                           if not key_name == '_filter_name'][0]
                        if 'bool' in elastic_match:
                            existing_match_phrase[inside_operator].extend(
                                elastic_match[inside_operator])
                        else:
                            existing_match_phrase[inside_operator].append(elastic_match)
                    else:
                        # if match phrase exists and is a single match, pop it
                        existing_single_match = branch_list.pop(existing_i)
                        if 'bool' in elastic_match:
                            inside_operator = [key_name for key_name in elastic_match.keys()
                                               if not key_name == '_filter_name'][0]
                            # if we have a bool, add the bool, add the popped match to bool
                            elastic_match[inside_operator].append(existing_single_match)
                            query['must'].append(elastic_match)
                        else:
                            # if  we have a single match, make new bool,
                            # add popped match and single match
                            matches = [existing_single_match, elastic_match]
                            query['must'].append({'bool': {elastic_operator: matches},
                                                  '_filter_name': current_filter_name})
        # remove our meta attribute so the query is elaticsearch-conform
        if initial_query is None:
            remove_all_dict_keys_from_mixed_dict(query, '_filter_name')
        return query

    def create_query_from_filters(self):
        # load filters from session
        query = self.load_filters()
        # add filters from request
        query = self.add_request_filters_to_elasticsearch_query(query)

        query = {
            'bool': query,
        }
        return query

    def add_request_filters_to_elasticsearch_query(self, elasticsearch_query):
        request = self.request

        window = None
        if self.request and self.request.GET.get('window', None):
            lon_min, lat_min, lon_max, lat_max = self.request.GET.get('window').split(',')
            try:
                lat_min, lat_max = float(lat_min), float(lat_max)
                lon_min, lon_max = float(lon_min), float(lon_max)
                # respect the 180th meridian
                if lon_min > lon_max:
                    lon_max, lon_min = lon_min, lon_max
                if lat_min > lat_max:
                    lat_max, lat_min = lat_min, lat_max
                window = (lon_min, lat_min, lon_max, lat_max)
            except ValueError:
                pass

        # add geo_point window match:
        if window:
            elasticsearch_query['filter'].append({
                "geo_bounding_box" : {
                    "geo_point" : {
                        "top_left" : {
                            "lat" : float(window[3]),
                            "lon" : float(window[0])
                        },
                        "bottom_right" : {
                            "lat" : float(window[1]),
                            "lon" : float(window[2])
                        }
                    }
                }
            })

        # collect a proper and authorized-for-that-user status list from the requet paramert
        request_status_list = self.request.GET.getlist('status', []) if self.request else []
        if self.request and self.request.user.is_staff:
            status_list_get = [int(status) for status in request_status_list
                               if (status.isnumeric() and
                                   int(status) in dict(ActivityBase.STATUS_CHOICES).keys())]
            if status_list_get:
                self.status_list = status_list_get

        elasticsearch_query['filter'].append({
            "bool": {
                'should': [
                    {'match': {'status': status}} for status in self.status_list
                ]
            }
        })

        # Public user?
        if not self.request or self.request.user.is_anonymous():
            elasticsearch_query['filter'].append({
                "bool": {
                    "filter": {
                        "term": {
                            "is_public": 'true'
                        }
                    }
                }
            })

        # TODO: these were at some point in the UI. add the missing filters!
        if self.request:
            request_filters = {
                'deal_scope': request.GET.getlist('deal_scope', ['domestic', 'transnational']),
                'limit': request.GET.get('limit'),
                'investor_country': request.GET.get('investor_country'),
                'investor_region': request.GET.get('investor_region'),
                'target_country': request.GET.get('target_country'),
                'target_region': request.GET.get('target_region'),
                'attributes': request.GET.getlist('attributes', []),
            }
        else:
            request_filters = {
                'deal_scope': ['domestic', 'transnational'],
                'limit': '',
                'investor_country': '',
                'investor_region': '',
                'target_country': '',
                'target_region': '',
                'attributes': [],
            }

        return elasticsearch_query

    def execute_elasticsearch_query(self, query, doc_type='deal', fallback=True, sort=[], aggs={}):
        from api.elasticsearch import es_search as es
        es.refresh_index()

        print('Elasticsearch query executed:\n')
        from pprint import pprint
        pprint(query)
        pprint(aggs)

        try:
            results = es.search(query, doc_type=doc_type, sort=sort, aggs=aggs)
        except Exception as e:
            raise
        return results

    def filter_returned_results(self, raw_result_list):
        """ Additional filtering and exclusion of unwanted results """
        result_list = []
        for raw_result in raw_result_list:
            result = raw_result['_source']
            #if not raw_result['_type'] in ('deal', 'location'):
            #    continue
            #if not 'point_lat' in result or not 'point_lon' in result:
            #    continue
            #if not result.get('intention', None): # TODO: should we hide results with no intention field value?
            #    continue
            result['id'] = raw_result['_id']
            result_list.append(result)

        # we have a special filter mode for status=STATUS_PENDING type searches,
        # if pending deals are to be shown, matched deals with status PENDING hide all other deals
        # with the same activity_identifier that are not PENDING
        if ActivityBase.STATUS_PENDING in self.status_list:
            pending_act_ids = [res['activity_identifier'] for res in result_list if res['status'] == ActivityBase.STATUS_PENDING]
            for i in reversed(range(len(result_list))):
                res = result_list[i]
                if not res['status'] == ActivityBase.STATUS_PENDING:
                    activity_identifier = res['activity_identifier']
                    # this match might be hidden if there is a pending match of PENDING status
                    if activity_identifier in pending_act_ids:
                        result_list = result_list[:-1]

        return result_list

    def disable_filters(self):
        """
        Disable current filters temporarily and set default filters
        :param request: 
        :return: 
        """
        # Backup
        self.request.session['disabled_filters'] = self.request.session.get('filters')
        self.request.session['disabled_set_default_filters'] = self.request.session.get(
            'set_default_filters', None)
        self.request.session['filters'] = {}
        if 'set_default_filters' in self.request.session:
            del(self.request.session['set_default_filters'])
        # FIXME: Move FilterWidgetMixin.set_default_filters to utils
        f = FilterWidgetMixin()
        f.request = self.request
        f.set_country_region_filter(self.request.GET.copy())
        f.set_default_filters(None, disabled_presets=[2,])

    def enable_filters(self):
        """
        Restore filters after being disabled by disable_filters()
        :return:
        """
        # Restore original filters
        self.request.session['filters'] = self.request.session.get('disabled_filters')
        if self.request.session['disabled_set_default_filters'] is not None:
            self.request.session['set_default_filters'] = self.request.session[
                'disabled_set_default_filters']
        del(self.request.session['disabled_filters'])
        del(self.request.session['disabled_set_default_filters'])


class UserListView(ListAPIView):
    """
    The users list view is used by the impersonate user feature of the editor.
    """
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class StatisticsView(ElasticSearchMixin,
                     APIView):
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
        target_country = request.GET.get('country', False)
        target_region = request.GET.get('region', False)
        disable_filters = request.GET.get('disable_filters', '') == '1'

        if disable_filters:
            self.disable_filters()
        query = self.create_query_from_filters()
        if target_country:
            query['bool']['filter'].append({
                'term': {
                    'target_country': target_country
                }
            })
        if target_region:
            query['bool']['filter'].append({
                'term': {
                    'target_region': target_region
                }
            })

        # Order by is set in aggregation
        aggs = {
            'current_negotiation_status': {
                'terms': {
                    'field': 'current_negotiation_status',
                    'size': 100,
                },
                'aggs': {
                    'deal_size_sum': {
                        'sum': {
                            'field': 'deal_size'
                        }
                    }
                }
            }
        }
        # Search deals
        results = self.execute_elasticsearch_query(query, doc_type='deal', fallback=False,
                                                   aggs=aggs)
        results = results['current_negotiation_status']['buckets']
        results = [[r['key'], r['doc_count'], r['deal_size_sum']['value']] for r in results]

        if disable_filters:
            self.enable_filters()
        return Response(results)


class LatestChangesView(ElasticSearchMixin,
                        APIView):
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
        target_country = request.GET.get('target_country', False)
        target_region = request.GET.get('target_region', False)
        n = int(request.GET.get('n', '20'))

        query = self.create_query_from_filters()
        if target_country:
            query['bool']['filter'].append({
                'term': {
                    'target_country': target_country
                }
            })
        if target_region:
            query['bool']['filter'].append({
                'term': {
                    'target_region': target_region
                }
            })


        # Search deals
        raw_results = self.execute_elasticsearch_query(query, doc_type='deal', fallback=False,
                                                       sort={'history_date': 'desc'})
        results = []
        for raw_result in raw_results[:n]:
            result = raw_result['_source']
            target_country = result['target_country_display']
            if len(target_country) > 0:
                target_country = target_country[0]
            results.append({
                "action": "add" if result['status'] == 2 else "change",
                "deal_id": result['activity_identifier'],
                "change_date": result['history_date'],
                "target_country": target_country
            })

        return Response(results)


class GlobalDealsView(ElasticSearchMixin, APIView):

    """
    Get all deals from elasticsearch index.
    Used within the map section.
    """
    doc_type = 'location'

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "window",
                required=False,
                location="query",
                description="Longitude min/max and Latitude min/max (e.g. 0,0,0,0)  ",
                schema=coreschema.String(),
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)

        # filter results
        result_list = self.filter_returned_results(raw_result_list)
        # parse results
        features = filter(None,
                          [self.create_feature_from_result(result) for result in result_list])
        response = Response(FeatureCollection(features))
        return response

    def create_feature_from_result(self, result):
        """ Create a GeoJSON-conform result. """

        intended_size = result.get('intended_size', None)
        intended_size = intended_size and intended_size[0] # saved as an array currently?
        contract_size = result.get('contract_size', None)
        contract_size = contract_size and contract_size[0] # saved as an array currently?
        production_size = result.get('production_size', None)
        production_size = production_size and production_size[0] # saved as an array currently?
        investor = result.get('operational_stakeholder', None)
        investor = investor and investor[0] # saved as an array currently?

        # Remove subcategories from intention
        intention = filter(lambda i: i not in INTENTION_EXCLUDE, result.get('intention', ['Unknown']))

        try:
            geometry = (float(result['point_lon']), float(result['point_lat']))
        except ValueError:
            return None
        return Feature(
            # Do not use ID for feature. Duplicate IDs lead to problems in
            # Openlayers.
            geometry=Point(geometry),
            properties={
                "url": reverse('deal_detail', kwargs={
                    'deal_id': result['activity_identifier']}),
                "intention": intention,
                "implementation": result.get('implementation_status', 'Unknown'),
                "intended_size": intended_size,
                "contract_size": contract_size,
                "production_size": production_size,
                "investor": investor,
                "identifier": result.get('activity_identifier'),
                "level_of_accuracy": result.get('level_of_accuracy', 'Unknown'),
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
        result_list = self.filter_returned_results(raw_result_list)

        target_countries = collections.defaultdict(PropertyCounter)

        for result in result_list:
            if result.get('target_country'):
                target_countries[result['target_country']].increment(**result)

        filter_country = self.request.GET.get('country_id')
        country_ids = [filter_country] if filter_country else target_countries.keys()
        countries = self.get_countries(*country_ids)

        features = []
        for country in countries:
            properties = {
                'name': country.name,
                'deals': target_countries[str(country.id)].counter,
                'url': country.get_absolute_url(),
                'centre_coordinates': [country.point_lon, country.point_lat],
            }
            properties.update(target_countries[str(country.id)].get_properties())
            features.append({
                'type': 'Feature',
                'id': country.code_alpha3,
                # 'geometry': json.loads(country.geom),
                'properties': properties
            })

        return Response(FeatureCollection(features))

    def get_countries(self, *ids):
        """
        Get countries with simplified geometry, to reduce size of response.
        """
        return Country.objects.defer('geom').filter(id__in=ids)


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
            ),
        ]
    )

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'type': 'Feature',
                'geometry': json.loads(self.get_queryset().simple_geom)
            }
        )

    def get_queryset(self):
        try:
            return Country.objects.extra(
                select={'simple_geom': 'ST_AsGeoJSON(ST_Simplify(geom, 0.01))'}
            ).get(
                id=self.request.GET.get('country_id')
            )
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
            ),
        ]
    )
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        polygon_field = kwargs.get('polygon_field')

        valid_polygon_fields = MapSettingsMixin.get_polygon_layers().keys()
        if polygon_field not in valid_polygon_fields:
            raise Http404

        # Reuse methods from GlobalDealsView

        # Get the basic query filter for Elasticsearch
        query = {}#self.create_query_from_filters()

        # Filter all objects which have an existing polygon field
        # TODO: Is there a better place and way for this?
        query = {
            'exists': {
                'field': polygon_field
            }
        }

        raw_result_list = self.execute_elasticsearch_query(query, self.doc_type)
        result_list = self.filter_returned_results(raw_result_list)

        features = []
        for result in result_list:
            feature = result.get(polygon_field)
            if feature is None:
                continue

            # Again, case sensitive: multipolygon in ES needs to be MultiPolygon
            # in GeoJSON.
            feature = json.loads(feature)
            feature['type'] = 'MultiPolygon'
            features.append(feature)

        return Response(FeatureCollection(features))
