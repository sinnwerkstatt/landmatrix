from pprint import pprint
from django.db import models, transaction
from django.utils.datastructures import MultiValueDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from migrate import V1, V2, load_project, BASE_PATH
from map_model import MapModel
from map_model_implementations import year_to_date

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')
load_project(BASE_PATH+'/land-matrix', 'editor')

from landmatrix.models import Language, ActivityAttributeGroup
from editor.models import A_Tag, A_Tag_Group, Comment


class MapTagGroups(MapModel):

    old_class = A_Tag_Group
    language = Language.objects.get(pk=1)

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False):

        cls._check_dependencies()
        cls._start_timer()
        cls.save = save

        tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity').filter(
            fk_activity__activity_identifier=147, fk_activity__version=4
        )
        cls.migrate_tag_group_set(tag_groups)

        cls._done = True
        cls._print_summary()

    @classmethod
    def migrate_tag_group_set(cls, tag_groups):
        for i, tag_group in enumerate(tag_groups):
            cls.migrate_tag_group(i, tag_group)

    @classmethod
    def migrate_tag_group(cls, i, tag_group):
        comments = get_comments(tag_group)

        relevant_tag_sets = [
            [tag_group.fk_a_tag],
            A_Tag.objects.using(V1).filter(fk_a_tag_group=tag_group).select_related('fk_a_key', 'fk_a_value'),
        ]
        for relevant_tags in relevant_tag_sets:

            attrs = {}

            for tag in relevant_tags:
                key = tag.fk_a_key.key
                value = tag.fk_a_value.value
                year = tag.fk_a_value.year
                print(i, key, value)
                if key in attrs:
                    cls.write_activity_attribute_group(attrs, comments, tag_group, year)
                attrs[key] = value

            if attrs:
                cls.write_activity_attribute_group(attrs, comments, tag_group, year)

        # cls._print_status(
        #     {
        #         key: value for key, value in tag_group.__dict__.items()
        #         if not callable(value) and not key.startswith('__')
        #     }, i)

    @classmethod
    def write_activity_attribute_group(cls, attrs, comments, tag_group, year):
        aag = ActivityAttributeGroup(
            fk_activity_id=tag_group.fk_activity.id, fk_language=cls.language,
            date=year_to_date(year), attributes=attrs, name=attrs.get('name')
        )
        if comments:
            aag.attributes.update({
                tag_group.fk_a_tag.fk_a_value.value + '_comment': '\n'.join(comments)
            })
            print(aag.attributes)
        if cls.save:
            aag.save(using=V2)



def get_comments(tag_group):
    queryset = Comment.objects.using(V1).filter(fk_a_tag_group=tag_group)
    return [comment.comment for comment in queryset]
