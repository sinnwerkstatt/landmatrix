
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

V1, V2 = 'v1_pg', 'v2'

BASE_PATH = '/home/lene/workspace/landmatrix'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
load_project(BASE_PATH+'/land-matrix', 'editor')

if __name__ == '__main__':

    from django.db.utils import ConnectionDoesNotExist

    try:

        from map_model_implementations import *
        from editor.models import ActivityAttributeGroup

        MapComment.map_all(save=True)

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
                map_class.map_all(save=True)

    except ConnectionDoesNotExist:
        print('You need to set CONVERT_DB to True in settings.py!')
    except AttributeError:
        print('You need to check out branch "postgres" of the old land-matrix project under '+BASE_PATH+'/land-matrix!')