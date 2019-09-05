#!/usr/bin/env python

from pprint import pprint

from django.core.management import BaseCommand

from apps.api.elasticsearch import es_search


class Command(BaseCommand):
    help = 'Update deal index for elasticsearch'
    es = None

    def handle(self, *args, **options):
        es = es_search
        es.refresh_index()
        
        query = {
                "bool": {
                    "should": [ # OR
                        {"bool": {'must': [ # AND
                            {'match': {'target_country': 276}},
                        ]}},
                        {"bool": {'must': [ # AND
                            {'match': {'target_country': 356}},
                        ]}},
                    ],
                    'must_not': {},
                    'filter': [
                        {"bool": {'should': [ # AND
                            {'match': {'status': 1234}},
                            {'match': {'status': 3234}}
                        ]}},
                    ]
                }
                
                #
            }
        
        """
        query = {
            "bool": {
                "must": {
                    "match_all": {}
                },
                "filter": [
                    {"geo_bounding_box" : {
                        "geo_point" : {
                            "top_left" : {
                                "lat" : 80.73,
                                "lon" : -84.1
                            },
                            "bottom_right" : {
                                "lat" : 20.01,
                                "lon" : -11.12
                            }
                        }
                    }},
                    {'exists': {'field': 'geo_point'}
                    },
                ]
            }
            
            #
        }
        """
        
        print('>>> searching for query')
        pprint(query)
        result = es.search(query)
        print('>>> received')
        pprint(result)
