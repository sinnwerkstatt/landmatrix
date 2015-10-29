from pprint import pprint
from django.db import models, transaction

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

        print(tag_groups)

        for i, tag_group in enumerate(tag_groups):
            cls.migrate_tag_group(i, tag_group)

    @classmethod
    def migrate_tag_group(cls, i, tag_group):
        attrs = {}
        aag = None
        comments = get_comments(tag_group)

        relevant_tag_sets = [
            A_Tag.objects.using(V1).filter(fk_a_tag_group=tag_group).select_related('fk_a_key', 'fk_a_value'),
            [tag_group.fk_a_tag]
        ]
        for relevant_tags in relevant_tag_sets:
            for tag in relevant_tags:
                key = tag.fk_a_key.key
                value = tag.fk_a_value.value
                year = tag.fk_a_value.year
                if not year in attrs:
                    attrs[year] = {}
                attrs[year][key] = value
                print(i, key, value, year)
        if attrs:
            for year, data in attrs.items():
                aag = ActivityAttributeGroup(
                    fk_activity_id=tag_group.fk_activity.id, fk_language=cls.language,
                    date=year_to_date(year), attributes=data
                )
        if aag:

            if comments:
                aag.attributes.update({
                    tag_group.fk_a_tag.fk_a_value.value + '_comment': '\n'.join(comments)
                })
#                print(tag_group.fk_a_tag.fk_a_value.value + '_comment:', ' '.join(comments))
            print(aag.attributes)

            if cls.save:
                aag.save(using=V2)

        # cls._print_status(
        #     {
        #         key: value for key, value in tag_group.__dict__.items()
        #         if not callable(value) and not key.startswith('__')
        #     }, i)


def get_comments(tag_group):
    queryset = Comment.objects.using(V1).filter(fk_a_tag_group=tag_group)
    return [comment.comment for comment in queryset]
