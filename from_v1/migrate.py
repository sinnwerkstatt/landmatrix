import traceback

from django.core.exceptions import ImproperlyConfigured

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def load_project(proj_path, app_name):

    import os, sys

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_name + ".settings")
    sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

V1, V2 = 'v1_my', 'v2'

BASE_PATH = '/home/lene/workspace/landmatrix'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
load_project(BASE_PATH+'/land-matrix', 'editor')

if __name__ == '__main__':

    from django.db.utils import ConnectionDoesNotExist

    try:

        from mapping import *
        # from mapping.map_tag_groups import MapTagGroups
        if V1 == 'v1_pg':
            from editor.models import ActivityAttributeGroup

        for map_class in [
            MapLanguage, MapStatus,
            MapActivity,
            MapActivityAttributeGroup,
            MapRegion,
            MapCountry,
            MapBrowseRule, MapBrowseCondition,
            MapStakeholder, MapPrimaryInvestor,
            MapInvolvement,
            MapStakeholderAttributeGroup,
            MapAgriculturalProduce, MapCrop, MapComment,
            MapInvestor, MapInvestorActivityInvolvement,
            MapStakeholderInvestor,
        ]:
            map_class.map_all(save=True)

        # a number of possible uses listed here as examples
        if False:
            MapActivity._done = True
            MapLanguage._done = True
            MapActivityAttributeGroup.map_all(save=True)
            MapAgriculturalProduce.map_all(save=True)
            MapCrop.map_all(save=True)

        if False:   # run to fix messed up country attributes on StakeholderAttributeGroup
            MapStakeholder._done = True
            MapLanguage._done = True
            MapStakeholderAttributeGroup.map_all(save=True)

        if False:   # example for migrating just one record
            MapActivityAttributeGroup.map(ActivityAttributeGroup.objects.using(V1).last().id)

        if False:   # migrate all data
            for map_class in [
                MapLanguage, MapStatus,
                MapActivity, MapActivityAttributeGroup,
                MapRegion, MapCountry, MapBrowseRule, MapBrowseCondition,
                MapStakeholder, MapPrimaryInvestor, MapInvolvement,
                MapStakeholderAttributeGroup,
                MapAgriculturalProduce, MapCrop, MapComment,
            ]:
                map_class.map_all(save=False)

    except ConnectionDoesNotExist as e:
        print('You need to set CONVERT_DB to True in settings.py!')
        print(e)
        traceback.print_tb(last_traceback)
    except AttributeError as e:
        print('You need to check out branch "postgres" of the old land-matrix project under')
        print(BASE_PATH+'/land-matrix!')
        print(e)
        traceback.print_tb(last_traceback)
    except (AttributeError, ImportError) as e:
        print('To migrate the original MySQL data you need to check out branch "master" of the')
        print('old land-matrix project under '+BASE_PATH+'/land-matrix!')
        print(e)
        traceback.print_tb(last_traceback)
    except ImproperlyConfigured:
        print('Do a "pip install mysqlclient" to install mysql drivers!')