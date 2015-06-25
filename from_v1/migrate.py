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

    print(os.getcwd(), application)

BASE_PATH = '/home/lene/workspace'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
import landmatrix.models

load_project(BASE_PATH+'/land-matrix', 'editor')
import editor.models

V1, V2 = 'v1_pg', 'v2'
MODELS = {
    V1: {
        editor.models.Language: [],
        editor.models.Activity: [],
        editor.models.ActivityAttributeGroup: [],
        editor.models.Status: [],
        editor.models.Stakeholder: [],
        editor.models.StakeholderAttributeGroup: [],
        editor.models.PrimaryInvestor: [],
        editor.models.Involvement: [],
        editor.models.Country: [],
        editor.models.Region: [],
        editor.models.BrowseRule: [],
        editor.models.BrowseCondition: [],
    },
    V2:    {
        landmatrix.models.Language: [],
        landmatrix.models.Activity: [],
        landmatrix.models.ActivityAttributeGroup: [],
        landmatrix.models.Status: [],
        landmatrix.models.Stakeholder: [],
        landmatrix.models.StakeholderAttributeGroup: [],
        landmatrix.models.PrimaryInvestor: [],
        landmatrix.models.Involvement: [],
        landmatrix.models.Country: [],
        landmatrix.models.Region: [],
        landmatrix.models.BrowseRule: [],
        landmatrix.models.BrowseCondition: [],
    }
}

class MapModel:

    attributes = { }

    @classmethod
    def map(cls, id):
        old = cls.old_class.objects.using(V1).get(id=id)
        new = cls.new_class()
        for (old_attribute, new_attribute) in cls.get_fields().items():
            setattr(new, new_attribute, getattr(old, old_attribute))

        if True:
            print(old, new)
        else:
            new.save(using=V2)

    @classmethod
    def map_all(cls):
        for id in cls.old_class.objects.using(V1).values('id'):
            cls.map(id['id'])

    @classmethod
    def get_fields(cls):
        fields = { cls.field_to_str(field): cls.field_to_str(field) for field in cls.old_class._meta.fields }
        fields.update(cls.attributes)
        return fields

    @classmethod
    def field_to_str(cls, field):
        return str(field).split('.')[-1]


class MapLanguage(MapModel):
    old_class = editor.models.Language
    new_class = landmatrix.models.Language

class MapStatus(MapModel):
    old_class = editor.models.Status
    new_class = landmatrix.models.Status

class MapActivity(MapModel):
    old_class = editor.models.Activity
    new_class = landmatrix.models.Activity
    attributes = { }

for version in [ V1, V2 ]:
    for cls in MODELS[version].keys():
        print(str(cls), cls.objects.using(version).count())

MapLanguage.map(editor.models.Language.objects.using(V1).last().id)
MapLanguage.map_all()

MapStatus.map(editor.models.Status.objects.using(V1).last().id)

MapActivity.map(editor.models.Activity.objects.using(V1).last().id)