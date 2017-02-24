#!/usr/bin/env python
import os
import sys

from django.core.management import BaseCommand
from pyelasticsearch import BulkError

from pprint import pprint
from landmatrix.models.activity import HistoricalActivity
from api.elasticsearch import es_search


class Command(BaseCommand):
    help = 'Update deal index for elasticsearch'
    es = None

    def handle(self, *args, **options):
        es = es_search
        es.refresh_index()
        
        query = {
            'query': {
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
                            {'match': {'status': 1}},
                            {'match': {'status': 3}}
                        ]}},
                    ]
                }
                
                #
            }
        }
        
        """
        query = {
            'query': {
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
        }
        """
        
        print('>>> searching for query')
        pprint(query)
        result = es.search(query)
        print('>>> received')
        pprint(result)
        