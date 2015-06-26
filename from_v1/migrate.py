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

BASE_PATH = '/home/lene/workspace'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
load_project(BASE_PATH+'/land-matrix', 'editor')

if __name__ == '__main__':

    from map_model_implementations import *
    from editor.models import ActivityAttributeGroup

#    MapActivityAttributeGroup.map(ActivityAttributeGroup.objects.using(V1).last().id)

    for map_class in [
        MapLanguage, MapStatus,
        MapActivity, MapActivityAttributeGroup,
        MapRegion, MapCountry, MapBrowseRule, MapBrowseCondition,
        MapStakeholder, MapPrimaryInvestor, MapInvolvement,
        MapStakeholderAttributeGroup,
    ]:
        map_class.map_all(save=True)
