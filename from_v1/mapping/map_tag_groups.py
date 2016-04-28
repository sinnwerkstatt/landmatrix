from django.db import transaction

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from migrate import V1, V2, load_project, BASE_PATH
from mapping.map_model import MapModel

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
load_project(BASE_PATH+'/land-matrix', 'editor')

from landmatrix.models import Language


class MapTagGroups(MapModel):

    key_value_lookup = None
    language = Language.objects.get(pk=1)

    @classmethod
    def map_all(cls, save=False, verbose=False):

        cls._check_dependencies()
        cls._start_timer()
        cls._save = save

        # migrate cached and/or generated values
        if cls.key_value_lookup:
            cls.migrate_lookup()

        # migrate original values. in case of conflict, original values overwrite cached values.
        cls._count = len(cls.tag_groups)
        cls.migrate_tag_group_set(cls.tag_groups)

        cls._done = True
        cls._print_summary()

    @classmethod
    @transaction.atomic(using=V2)
    def migrate_tag_group_set(cls, tag_groups):
        for i, tag_group in enumerate(tag_groups):
            cls.migrate_tag_group(i, tag_group)

    @classmethod
    def migrate_tag_group(cls, i, tag_group):

        for relevant_tags in cls.relevant_tag_sets(tag_group):
            cls.migrate_tags(relevant_tags, tag_group)

        cls._print_status({ key: value for key, value in tag_group.__dict__.items() if not callable(value) and not key.startswith('__') }, i)


