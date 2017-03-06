import json

import collections
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from grid.views.activity_protocol import ActivityQuerySet
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.latest_changes_query_set import LatestChangesQuerySet
from api.query_sets.statistics_query_set import StatisticsQuerySet
from api.serializers import DealSerializer, UserSerializer
from api.pagination import FakeQuerySetPagination
from api.views.base import FakeQuerySetListView
from landmatrix.models import Country
from landmatrix.models.activity import ActivityBase

from django.conf import settings

from geojson import FeatureCollection, Feature, Point, MultiPoint
from api.filters import load_filters, FILTER_FORMATS_ELASTICSEARCH,\
    FILTER_FORMATS_SQL
from grid.forms.choices import INTENTION_AGRICULTURE_MAP, INTENTION_FORESTRY_MAP

User = get_user_model()

INTENTION_EXCLUDE = list(INTENTION_AGRICULTURE_MAP.keys())
INTENTION_EXCLUDE.extend(list(INTENTION_FORESTRY_MAP.keys()))

class UserListView(ListAPIView):
    '''
    The users list view is used by the impersonate user feature of the editor.
    '''
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class StatisticsListView(FakeQuerySetListView):
    fake_queryset_class = StatisticsQuerySet


class ActivityListView(FakeQuerySetListView):
    fake_queryset_class = ActivityQuerySet


class LatestChangesListView(FakeQuerySetListView):
    '''
    Lists recent changes to the database (add, change, delete or comment)
    '''
    fake_queryset_class = LatestChangesQuerySet


class DealListView(FakeQuerySetListView):
    fake_queryset_class = DealsQuerySet
    serializer_class = DealSerializer
    pagination_class = FakeQuerySetPagination

    def get_queryset(self):
        '''
        Don't call all on the queryset, so that it is passed to the paginator
        before evaluation.
        '''
        return self.fake_queryset_class(self.request)


class GlobalDealsView(APIView):
    
    # default status are the public ones. will only get replaced if well formed and allowed
    status_list = ActivityBase.PUBLIC_STATUSES
    
    def get_queryset(self):
        '''
        Don't call all on the queryset, so that it is passed to the paginator
        before evaluation.
        '''
        return self.fake_queryset_class(self.request)
    
    def create_query_from_filters(self):
        # load filters from session
        elasticsearch_query = load_filters(self.request, filter_format=FILTER_FORMATS_ELASTICSEARCH)
        # add filters from request
        elasticsearch_query = self.add_request_filters_to_elasticsearch_query(elasticsearch_query)
        
        query = {'bool': elasticsearch_query}
        return query
    
    def add_request_filters_to_elasticsearch_query(self, elasticsearch_query):
        request = self.request
        
        window = None
        if self.request.GET.get('window', None):
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
        request_status_list = self.request.GET.getlist('status', []) 
        if self.request.user.is_staff:
            status_list_get = [int(status) for status in request_status_list if (status.isnumeric() and int(status) in dict(ActivityBase.STATUS_CHOICES).keys())]
            if status_list_get:
                self.status_list = status_list_get
                
        elasticsearch_query['filter'].append({
            "bool": {
                'should': [
                    {'match': {'status': status}} for status in self.status_list
                ]
            }
        })
        
        # TODO: these were at some point in the UI. add the missing filters!
        request_filters = {
            'deal_scope': request.GET.getlist('deal_scope', ['domestic', 'transnational']),
            'limit': request.GET.get('limit'),
            'investor_country': request.GET.get('investor_country'),
            'investor_region': request.GET.get('investor_region'),
            'target_country': request.GET.get('target_country'),
            'target_region': request.GET.get('target_region'),
            'attributes': request.GET.getlist('attributes', []),
        }
        
        return elasticsearch_query
        
    def get(self, request, *args, **kwargs):
        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query)    
        
        # filter results
        result_list = self.filter_returned_results(raw_result_list)
        # parse results
        features = [self.create_feature_from_result(result) for result in result_list]
        response = Response(FeatureCollection(features))
        return response
    
    def execute_elasticsearch_query(self, query):
        from api.elasticsearch import es_search as es
        es.refresh_index()
        
        print('\n\n\n>> This is the executed elasticsearch query:\n')
        from pprint import pprint
        pprint(query)
        
        try:
            raw_result_list = es.search(query)
            if settings.DEBUG and len(raw_result_list) == 0:
                raise(Exception('NoResultsForQuery-DebugException! I am raising this because the query got no results and was probably malformed.'))
        except Exception as e:
            if settings.DEBUG:
                print('\n\n>>>>>>> Error! There was an error when querying elasticsearch with the current filters!')
                print('               Falling back to a match-all query.')
                print('               WARNING: YOUR RESULTS ARE NOT THOSE OF A FILTERED QUERY!\n\n')
                print('               Exception was:\n')
                print(e)
                print('\n\n')
                
                match_all_query = { "match_all": {} }
                raw_result_list = es.search(match_all_query)
            else:
                raise
            
        return raw_result_list
    
    def filter_returned_results(self, raw_result_list):
        """ Additional filtering and exclusion of unwanted results """
        result_list = []
        for raw_result in raw_result_list:
            result = raw_result['_source']
            if not raw_result['_type'] == 'deal':
                continue
            if not 'point_lat' in result or not 'point_lon' in result:
                continue
            if not result.get('intention', None): # TODO: should we hide results with no intention field value?
                continue
            result_list.append(result)
        
        # we have a special filter mode for status=STATUS_PENDING type searches, 
        # if pending deals are to be shown, matched deals with status PENDING hide all other deals
        # with the same activity_identifier that are not PENDING
        if ActivityBase.STATUS_PENDING in self.status_list:
            pending_act_ids = [res['activity_identifier'] for res in result_list if res['status'] == ActivityBase.STATUS_PENDING]
            for i in reversed(range(len(result_list))):
                res = result_list[i]
                if not res['status'] == ActivityBase.STATUS_PENDING:
                    actitvity_identifier = res['activity_identifier']
                    # this match might be hidden if there is a pending match of PENDING status
                    if actitvity_identifier in pending_act_ids:
                        print('removed ', res)
                        result_list = result_list[:-1]
        
        return result_list

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
        intention = filter(lambda i: i not in INTENTION_EXCLUDE, result.get('intention', []))

        geometry = (float(result['point_lon']), float(result['point_lat']))
        return Feature(
            # Do not use ID for feature. Duplicate IDs lead to problems in
            # Openlayers.
            geometry=Point(geometry),
            properties={
                "url": "/en/deal/%s/" % result['historical_activity_id'],
                "intention": intention,
                "implementation": result.get('implementation_status'),
                "intended_size": intended_size,
                "contract_size": contract_size,
                "production_size": production_size,
                "investor": investor,
                "identifier": result.get('activity_identifier'),
            },
        )


class CountryDealsView(GlobalDealsView, APIView):
    """
    Group deals by country
    """

    def get_country_properties(self):
        """
        Helper to increment count of properties. One Properties-class is set
        per country.
        """
        class PropertyCounter(dict):
            # mapping of keys from elasticsearch <-> legend.
            properties = {
                'intention': 'intention',
                'implementation': 'negotiation_status',
                'accuracy': 'level_of_accuracy',
            }

            def __init__(self):
                super().__init__()
                self.counter = 0
                for prop in self.properties.keys():
                    setattr(self, prop, collections.defaultdict(int))

            def increment(self, **data):
                for key, es_key in self.properties.items():
                    values = data.get(es_key)
                    prop = getattr(self, key)
                    if isinstance(values, list):
                        for val in values:
                            prop[val] += 1
                    else:
                        prop[values] += 1
                self.counter += 1

            def get_properties(self):
                return {prop: getattr(self, prop) for prop in self.properties}

        return PropertyCounter

    def get_countries(self, *ids):
        """
        Get countries with simplified geometry, to reduce size of response.
        """
        return Country.objects.extra(
            select={'simple_geom': 'ST_AsGeoJSON(ST_SimplifyVW(geom, 10000))'}
        ).filter(id__in=ids)

    def get(self, request, *args, **kwargs):
        """
        Return grouped deals by country.
        """

        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query)

        # filter results
        result_list = self.filter_returned_results(raw_result_list)

        target_countries = collections.defaultdict(self.get_country_properties())

        for result in result_list:
            if result.get('target_country'):
                target_countries[result['target_country']].increment(**result)

        filter_country = self.request.GET.get('country_id')
        country_ids = [filter_country] if filter_country else target_countries.keys()
        countries = self.get_countries(*country_ids)[0:10]

        features = []
        for country in countries:
            features.append({
                'type': 'Feature',
                'id': country.code_alpha3,
                'geometry': json.loads(country.simple_geom),
                'properties': {
                    'name': country.name,
                    'deals': target_countries[str(country.id)].counter,
                    'url': country.get_absolute_url(),
                    'centre_coordinates': [country.point_lon, country.point_lat],
                    **target_countries[str(country.id)].get_properties()
                }
            })

        return Response(FeatureCollection(features))
