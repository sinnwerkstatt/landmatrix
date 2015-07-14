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

from landmatrix.models import *


records = Activity.objects.filter(fk_status__name__in=['active', 'overwritten'])
print(len(records))

if False:
    records = Activity.objects. \
        filter(fk_status__name__in=['active', 'overwritten']). \
        filter(activityattributegroup__attributes__contains=['intention'])[:5]
    from django.contrib.admin.util import NestedObjects
    collector = NestedObjects(using="default") #database name
    for object in records:
        collector.collect([object]) #list of objects. single one won't do
        print(collector.data.keys())
        print(len(collector.data[ActivityAttributeGroup]))
        print([aag for aag in collector.data[ActivityAttributeGroup] if 'intention' in aag.attributes])
        print('*'*80)
