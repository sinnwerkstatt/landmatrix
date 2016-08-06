import pprint

from setuptools.command.setopt import setopt

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

#
# make script run in django context.
#
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

#
# actual script follows.
#
from landmatrix.models.activity_attribute_group import ActivityAttribute
import json
import argparse


def write_comparison_data(filename, data):
    with open(filename, 'w+') as f:
        f.write(json.dumps(data)+"\n")


def read_comparison_data(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate', action="store_true")
    parser.add_argument('-c', '--compare', action="store_true")
    parser.add_argument('-f', '--file')

    return parser.parse_args()


#def generate(groups):
#    attributes = {}
#    for group in groups:
#        for key, value in group['attributes'].items():
#            if key not in attributes:
#                attributes[key] = [value]
#            else:
#                attributes[key].append(value)
#    for attribute, values in attributes.items():
#        attributes[attribute] = list(set(values))
#    return attributes


def compare(attributes, reference_attributes):
    different = False
    for key in attributes:
        if set(attributes[key]) != set(reference_attributes[key]):
            print(key)
            pprint.pprint(attributes[key])
            pprint.pprint(reference_attributes[key])
            different = True
    return different

if __name__ == '__main__':

    args = parse_args()

    activity_ids = sorted(set(ActivityAttribute.objects.values_list('fk_activity_id', flat=True)))

    attributes = {}
    for id in activity_ids:
        attrs = ActivityAttribute.objects.filter(fk_activity_id=id).values('name', 'value')
        attributes[id] = dict(attrs)

    if args.generate:
        if args.file:
            write_comparison_data(args.file, attributes)
        else:
            pprint.pprint(attributes, width=120)

    elif args.compare:
        reference_data = read_comparison_data(args.file)

        for id in attributes.keys():
            if compare(attributes[id], reference_data[str(id)]):
                print(id)
