__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import os
import pprint
from django.http import HttpRequest
from django.utils.datastructures import MultiValueDict
import json

import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


proj_path = os.path.join(os.path.dirname(__file__), "../..")
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "landmatrix.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from global_app.views import DummyActivityProtocol


def read_data(filename):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/' + filename, 'r') as f:
        lines = f.readlines()
    parameters = eval(lines[1])
    records = eval(lines[2])
    return (parameters['data'][0], records[:10])
    return ((parse_post_data(parameters)), records[:10])


def parse_post_data(parameters):
    null = None
    return eval(parameters['data'][0])

def considered_equal(field, expected, actual):
    if field == 2:
        return expected == actual
    elif field == 10:
        return expected == actual
    else:
        return expected == actual

if __name__ == '__main__':
    for filename in ['all_deals.out']:
        postdata, records = read_data(filename)
        protocol = DummyActivityProtocol()
        request = HttpRequest()
        request.POST = {'data': postdata}
        res = protocol.dispatch(request, action="list_group").content
        query_result = json.loads(res.decode())['activities'][:10]
        for id in range(0, len(records)):
            for j in range(0, len(records[id])):
                if not considered_equal(j, records[id][j], query_result[id][j]):
                    print("ID: %i, field %i: expected %s, got %s" % (records[id][1], j, str(records[id][j]), str(query_result[id][j])))

