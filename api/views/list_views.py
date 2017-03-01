import json

import collections
from django.contrib.auth import get_user_model
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin
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
from map.views import MapSettingsMixin
from landmatrix.models.activity import ActivityBase

from django.conf import settings

from geojson import FeatureCollection, Feature, Point, MultiPoint
from api.filters import load_filters, FILTER_FORMATS_ELASTICSEARCH,\
    FILTER_FORMATS_SQL

User = get_user_model()


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

        geometry = (float(result['point_lon']), float(result['point_lat']))
        return Feature(
            # Do not use ID for feature. Duplicate IDs lead to problems in
            # Openlayers.
            geometry=Point(geometry),
            properties={
                "url": "/en/deal/%s/" % result['activity_identifier'],
                "intention": result.get('intention'),
                "implementation": 'in_operation', # TODO: where to get this from?
                "intended_size": intended_size,
                "contract_size": contract_size,
                "production_size": None,
                "investor": "Investor-Name-Where-Do-I-Get-This",
                "identifier": result.get('activity_identifier'),
            },
        )


class _Mock_GlobalDealsView(APIView):
    """
    Mock required response
    """
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        # Corresponds to deal_id in api/deals.json
                        "id": 3790,
                        "properties": {
                            "url": "/en/deal/3790/",
                            "intention": [
                                # Only top categories (eg. no "biofuels")
                                "agriculture"
                            ],
                            "implementation": 'in_operation',
                            "intended_size": 30000,
                            "contract_size": 30000,
                            "production_size": None,
                            "investor": "Unknown (Agro Energy Développement)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -4.82596920,
                                14.49680350
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1480,
                        "properties": {
                            "url": "/en/deal/1480/",
                            "intention": [
                                "agriculture"
                            ],
                            "implementation": 'in_operation',
                            "intended_size": 30000,
                            "contract_size": 30000,
                            "production_size": None,
                            "investor": "Unknown (Southern Global Inc.)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -4.82596920,
                                14.49680350
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1474,
                        "properties": {
                            "url": "/en/deal/1474/",
                            "intention": [
                                "agriculture"
                            ],
                            "implementation": 'abandoned',
                            "intended_size": 100000,
                            "contract_size": 25000,
                            "production_size": None,
                            "investor": "Unknown (Libyan African Investment Portfolio, Unnamed investor 212)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -5.16607226,
                                14.17691062
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 3326,
                        "properties": {
                            "url": "/en/deal/3326/",
                            "intention": [
                                "mining"
                            ],
                            "implementation": 'unknown',
                            "intended_size": None,
                            "contract_size": None,
                            "production_size": None,
                            "investor": "Unknown (AngloGold Ashanti , Government, Randgold Resources)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -6.28333300,
                                11.91666700
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1470,
                        "properties": {
                            "url": "/en/deal/1470/",
                            "intention": [
                                "agriculture"
                            ],
                            "implementation": 'unknown',
                            "intended_size": 1000,
                            "contract_size": 1000,
                            "production_size": None,
                            "investor": "Mali Folkcenter"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -7.43700000,
                                10.99000000
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1467,
                        "properties": {
                            "url": "/en/deal/1467/",
                            "intention": [
                                "agriculture",
                                "renewable_energy"
                            ],
                            "implementation": 'in_operation',
                            "intended_size": 20000,
                            "contract_size": 20000,
                            "production_size": None,
                            "investor": "N'Sukula"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -6.10233000,
                                14.03790000
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1508,
                        "properties": {
                            "url": "/en/deal/1508/",
                            "intention": [
                                "agriculture",
                                "forestry"
                            ],
                            "implementation": 'unknown',
                            "intended_size": None,
                            "contract_size": None,
                            "production_size": None,
                            "investor": "Jatropha Mali Initiative JMI"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -9.48472300,
                                13.04114000
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1486,
                        "properties": {
                            "url": "/en/deal/1486/",
                            "intention": [
                                "agriculture",
                                "conservation",
                                "forestry"
                            ],
                            "implementation": 'in_operation',
                            "intended_size": 205700,
                            "contract_size": 205700,
                            "production_size": None,
                            "investor": "Agro Industrie Développement SA (AID-SA)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -8.15000000,
                                11.18333330
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1478,
                        "properties": {
                            "url": "/en/deal/1478/",
                            "intention": [
                                "agriculture"
                            ],
                            "implementation": 'in_operation',
                            "intended_size": 160000,
                            "contract_size": 10000,
                            "production_size": None,
                            "investor": "PETROTECH – ffn AGRO MALI SA"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -7.56666670,
                                12.86666670
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1481,
                        "properties": {
                            "url": "/en/deal/1481/",
                            "intention": [
                                "agriculture",
                                "other"
                            ],
                            "implementation": 'abandoned',
                            "intended_size": 22441,
                            "contract_size": 22441,
                            "production_size": None,
                            "investor": "Unknown (Millenium Challenge Corporation)"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -4.82596920,
                                14.49680350
                            ]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 1501,
                        "properties": {
                            "url": "/en/deal/1501/",
                            "intention": [
                                "agriculture",
                                "forestry"
                            ],
                            "implementation": 'unknown',
                            "intended_size": None,
                            "contract_size": None,
                            "production_size": None,
                            "investor": "Koulikoro Biocarburant SA"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -7.56666670,
                                12.86666670
                            ]
                        }
                    }
                ]
            })


class CountryDealsView(APIView):
    """
    Mock required response
    """
    def get(self, request, *args, **kwargs):
        """
        Label keywords (intention, agriculture etc.) must match IDs of
        MapSettingsMixin.get_legend().
        """
        return Response(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "MLI",
                        "properties": {
                            "name": "Mali",
                            "deals": 12,
                            "url": "/en/mali",
                            "intention": {
                                "agriculture": 4,
                                "renewable_energy": 2,
                                "mining": 1,
                                "forestry": 1,
                                "tourism": 1,
                                "industry": 1,
                                "conservation": 1,
                                "other": 1
                            },
                            "accuracy": {
                                "1km": 6,
                                "10km": 2
                            },
                            "implementation": {
                                "not_started": 1,
                                "startup": 1,
                                "in_operation": 3,
                                "abandoned": 3,
                                "unknown": 2
                            },
                            # this is a voluntary field, as override for the
                            # 'calculated' centre where the info is displayed.
                            "centre_coordinates": [-439000, 2000000]
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[-12.17075, 14.616834],
                                 [-11.834208, 14.799097],
                                 [-11.666078, 15.388208],
                                 [-11.349095, 15.411256],
                                 [-10.650791, 15.132746],
                                 [-10.086846, 15.330486],
                                 [-9.700255, 15.264107], [-9.550238, 15.486497],
                                 [-5.537744, 15.50169], [-5.315277, 16.201854],
                                 [-5.488523, 16.325102], [-5.971129, 20.640833],
                                 [-6.453787, 24.956591], [-4.923337, 24.974574],
                                 [-1.550055, 22.792666], [1.823228, 20.610809],
                                 [2.060991, 20.142233], [2.683588, 19.85623],
                                 [3.146661, 19.693579], [3.158133, 19.057364],
                                 [4.267419, 19.155265], [4.27021, 16.852227],
                                 [3.723422, 16.184284], [3.638259, 15.56812],
                                 [2.749993, 15.409525], [1.385528, 15.323561],
                                 [1.015783, 14.968182], [0.374892, 14.928908],
                                 [-0.266257, 14.924309], [-0.515854, 15.116158],
                                 [-1.066363, 14.973815], [-2.001035, 14.559008],
                                 [-2.191825, 14.246418], [-2.967694, 13.79815],
                                 [-3.103707, 13.541267], [-3.522803, 13.337662],
                                 [-4.006391, 13.472485], [-4.280405, 13.228444],
                                 [-4.427166, 12.542646], [-5.220942, 11.713859],
                                 [-5.197843, 11.375146], [-5.470565, 10.95127],
                                 [-5.404342, 10.370737], [-5.816926, 10.222555],
                                 [-6.050452, 10.096361], [-6.205223, 10.524061],
                                 [-6.493965, 10.411303], [-6.666461, 10.430811],
                                 [-6.850507, 10.138994], [-7.622759, 10.147236],
                                 [-7.89959, 10.297382], [-8.029944, 10.206535],
                                 [-8.335377, 10.494812], [-8.282357, 10.792597],
                                 [-8.407311, 10.909257], [-8.620321, 10.810891],
                                 [-8.581305, 11.136246], [-8.376305, 11.393646],
                                 [-8.786099, 11.812561], [-8.905265, 12.088358],
                                 [-9.127474, 12.30806], [-9.327616, 12.334286],
                                 [-9.567912, 12.194243], [-9.890993, 12.060479],
                                 [-10.165214, 11.844084],
                                 [-10.593224, 11.923975],
                                 [-10.87083, 12.177887],
                                 [-11.036556, 12.211245],
                                 [-11.297574, 12.077971],
                                 [-11.456169, 12.076834],
                                 [-11.513943, 12.442988],
                                 [-11.467899, 12.754519],
                                 [-11.553398, 13.141214],
                                 [-11.927716, 13.422075],
                                 [-12.124887, 13.994727],
                                 [-12.17075, 14.616834]]]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": "BFA",
                        "properties": {
                            "name": "Burkina Faso",
                            "deals": 3,
                            "url": "/en/bfa",
                            "intention": {
                                "agriculture": 3,
                                "renewable_energy": 1
                            },
                            "accuracy": {
                                "1km": 6,
                                "10km": 2
                            },
                            "implementation": {
                                "in_operation": 2,
                                "unknown": 1
                            },
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates":
                                [[[-2.827496, 9.642461], [-3.511899, 9.900326],
                                  [-3.980449, 9.862344], [-4.330247, 9.610835],
                                  [-4.779884, 9.821985], [-4.954653, 10.152714],
                                  [-5.404342, 10.370737], [-5.470565, 10.95127],
                                  [-5.197843, 11.375146],
                                  [-5.220942, 11.713859],
                                  [-4.427166, 12.542646],
                                  [-4.280405, 13.228444],
                                  [-4.006391, 13.472485],
                                  [-3.522803, 13.337662],
                                  [-3.103707, 13.541267], [-2.967694, 13.79815],
                                  [-2.191825, 14.246418],
                                  [-2.001035, 14.559008],
                                  [-1.066363, 14.973815],
                                  [-0.515854, 15.116158],
                                  [-0.266257, 14.924309], [0.374892, 14.928908],
                                  [0.295646, 14.444235], [0.429928, 13.988733],
                                  [0.993046, 13.33575], [1.024103, 12.851826],
                                  [2.177108, 12.625018], [2.154474, 11.94015],
                                  [1.935986, 11.64115], [1.447178, 11.547719],
                                  [1.24347, 11.110511], [0.899563, 10.997339],
                                  [0.023803, 11.018682], [-0.438702, 11.098341],
                                  [-0.761576, 10.93693], [-1.203358, 11.009819],
                                  [-2.940409, 10.96269], [-2.963896, 10.395335],
                                  [-2.827496, 9.642461]]]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": "CIV",
                        "properties": {
                            "name": "Ivory Coast",
                            "deals": 9,
                            "url": "/en/civ",
                            "intention": {
                                "agriculture": 9,
                                "renewable_energy": 1,
                                "forestry": 1
                            },
                            "accuracy": {
                                "1km": 6,
                                "10km": 2
                            },
                            "implementation": {
                                "in_operation": 6,
                                "not_started": 2,
                                "unknown": 1
                            },
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[-2.856125, 4.994476], [-3.311084, 4.984296],
                                 [-4.00882, 5.179813], [-4.649917, 5.168264],
                                 [-5.834496, 4.993701], [-6.528769, 4.705088],
                                 [-7.518941, 4.338288], [-7.712159, 4.364566],
                                 [-7.635368, 5.188159], [-7.539715, 5.313345],
                                 [-7.570153, 5.707352], [-7.993693, 6.12619],
                                 [-8.311348, 6.193033], [-8.60288, 6.467564],
                                 [-8.385452, 6.911801], [-8.485446, 7.395208],
                                 [-8.439298, 7.686043], [-8.280703, 7.68718],
                                 [-8.221792, 8.123329], [-8.299049, 8.316444],
                                 [-8.203499, 8.455453], [-7.8321, 8.575704],
                                 [-8.079114, 9.376224], [-8.309616, 9.789532],
                                 [-8.229337, 10.12902], [-8.029944, 10.206535],
                                 [-7.89959, 10.297382], [-7.622759, 10.147236],
                                 [-6.850507, 10.138994], [-6.666461, 10.430811],
                                 [-6.493965, 10.411303], [-6.205223, 10.524061],
                                 [-6.050452, 10.096361], [-5.816926, 10.222555],
                                 [-5.404342, 10.370737], [-4.954653, 10.152714],
                                 [-4.779884, 9.821985], [-4.330247, 9.610835],
                                 [-3.980449, 9.862344], [-3.511899, 9.900326],
                                 [-2.827496, 9.642461], [-2.56219, 8.219628],
                                 [-2.983585, 7.379705], [-3.24437, 6.250472],
                                 [-2.810701, 5.389051], [-2.856125, 4.994476]]]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": "GHA",
                        "properties": {
                            "name": "Ghana",
                            "deals": 41,
                            "url": "/en/ghana",
                            "intention": {
                                "agriculture": 37,
                                "renewable_energy": 3,
                                "conservation": 1,
                                "forestry": 6
                            },
                            "accuracy": {
                                "1km": 6,
                                "10km": 2
                            },
                            "implementation": {
                                "startup": 7,
                                "not_started": 4,
                                "abandoned": 3,
                                "in_operation": 20,
                                "unknown": 7
                            },
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[1.060122, 5.928837], [-0.507638, 5.343473],
                                 [-1.063625, 5.000548], [-1.964707, 4.710462],
                                 [-2.856125, 4.994476], [-2.810701, 5.389051],
                                 [-3.24437, 6.250472], [-2.983585, 7.379705],
                                 [-2.56219, 8.219628], [-2.827496, 9.642461],
                                 [-2.963896, 10.395335], [-2.940409, 10.96269],
                                 [-1.203358, 11.009819], [-0.761576, 10.93693],
                                 [-0.438702, 11.098341], [0.023803, 11.018682],
                                 [-0.049785, 10.706918], [0.36758, 10.191213],
                                 [0.365901, 9.465004], [0.461192, 8.677223],
                                 [0.712029, 8.312465], [0.490957, 7.411744],
                                 [0.570384, 6.914359], [0.836931, 6.279979],
                                 [1.060122, 5.928837]]]
                        }
                    },
                    {
                        "type": "Feature",
                        "id": "TGO",
                        "properties": {
                            "name": "Togo",
                            "deals": 10,
                            "url": "/en/togo",
                            "intention": {
                                "agriculture": 9,
                                "tourism": 4
                            },
                            "accuracy": {
                                "1km": 6,
                                "10km": 2
                            },
                            "implementation": {
                                "startup": 4,
                                "in_operation": 6
                            },
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[1.865241, 6.142158], [1.060122, 5.928837],
                                 [0.836931, 6.279979], [0.570384, 6.914359],
                                 [0.490957, 7.411744], [0.712029, 8.312465],
                                 [0.461192, 8.677223], [0.365901, 9.465004],
                                 [0.36758, 10.191213], [-0.049785, 10.706918],
                                 [0.023803, 11.018682], [0.899563, 10.997339],
                                 [0.772336, 10.470808], [1.077795, 10.175607],
                                 [1.425061, 9.825395], [1.463043, 9.334624],
                                 [1.664478, 9.12859], [1.618951, 6.832038],
                                 [1.865241, 6.142158]]]
                        }
                    }
                ]
            }
        )
