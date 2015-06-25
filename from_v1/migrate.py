__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import os, sys

def load_project(proj_path, app_name):

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_name + ".settings")
    sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

BASE_PATH = '/home/lene/workspace'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
import landmatrix.models

load_project(BASE_PATH+'/land-matrix', 'editor')
import editor.models

V1, V2 = 'v1_pg', 'v2'
MODELS = {
    V1: {
        editor.models.PrimaryInvestor: [],
        editor.models.Involvement: [],
        editor.models.Country: [],
        editor.models.Region: [],
        editor.models.BrowseRule: [],
        editor.models.BrowseCondition: [],
    },
    V2:    {
        landmatrix.models.PrimaryInvestor: [],
        landmatrix.models.Involvement: [],
        landmatrix.models.Country: [],
        landmatrix.models.Region: [],
        landmatrix.models.BrowseRule: [],
        landmatrix.models.BrowseCondition: [],
    }
}

if __name__ == '__main__':

    from map_model import MapModel

    class MapLanguage(MapModel):
        old_class = editor.models.Language
        new_class = landmatrix.models.Language

    class MapStatus(MapModel):
        old_class = editor.models.Status
        new_class = landmatrix.models.Status

    class MapActivity(MapModel):
        old_class = editor.models.Activity
        new_class = landmatrix.models.Activity

    def year_to_date(year):
        return None if year is None else str(year)+'-01-07'

    class MapActivityAttributeGroup(MapModel):
        old_class = editor.models.ActivityAttributeGroup
        new_class = landmatrix.models.ActivityAttributeGroup
        attributes = {
            'activity': 'fk_activity',
            'language': 'fk_language',
            'year': ('date', year_to_date)
        }

    class MapStakeholder(MapModel):
        old_class = editor.models.Stakeholder
        new_class = landmatrix.models.Stakeholder

    class MapStakeholderAttributeGroup(MapModel):
        old_class = editor.models.StakeholderAttributeGroup
        new_class = landmatrix.models.StakeholderAttributeGroup
        attributes = {
            'stakeholder': 'fk_stakeholder',
            'language': 'fk_language',
        }


    for version in [ V1, V2 ]:
        for cls in MODELS[version].keys():
            print(str(cls), cls.objects.using(version).count())

    MapLanguage.map_all()

    MapStatus.map_all()

    MapActivity.map(editor.models.Activity.objects.using(V1).last().id)

    # map a random ActivityAttributeGroup
    MapActivityAttributeGroup.map(editor.models.ActivityAttributeGroup.objects.using(V1).last().id)
    # map an ActivityAttributeGroup with a year
    MapActivityAttributeGroup.map(315980)

    MapStakeholder.map(editor.models.Stakeholder.objects.using(V1).last().id, printit=True)

    MapStakeholderAttributeGroup.map(editor.models.StakeholderAttributeGroup.objects.using(V1).last().id, printit=True)