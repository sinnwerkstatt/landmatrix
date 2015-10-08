__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.tests.api_test_functions import ApiTestFunctions
from api.tests.api_test_base import ApiTestExtendedBase


class TastyPieTest(ApiTestFunctions, ApiTestExtendedBase):
    PREFIX = '/en/api/api/'
    POSTFIX = '/?format=json'
    INFIX = '/'
    URI_INDEX = 'resource_uri'
    RESULTS_INDEX = 'objects'
    MODELS = [ 'involvement', 'activity', 'stakeholder', 'primaryinvestor', 'status', 'activityattributegroup']
