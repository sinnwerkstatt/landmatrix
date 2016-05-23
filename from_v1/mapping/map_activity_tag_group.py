from pprint import pprint

from django.db.models.aggregates import Max
from functools import lru_cache
from mapping.map_activity import MapActivity
from mapping.aux_functions import year_to_date
from migrate import V1, V2
from mapping.map_tag_groups import MapTagGroups

from landmatrix.models import Language, Activity, ActivityAttributeGroup
import landmatrix.models

if V1 == 'v1_my':
    from old_editor.models import A_Tag, A_Tag_Group, A_Key_Value_Lookup, Comment

from django.db import transaction

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapActivityTagGroupBase:

    @classmethod
    def write_activity_attribute_group_with_comments(cls, attrs, tag_group, year, name):
        if (len(attrs) == 1) and attrs.get('name'):
            return

        from mapping.map_activity_attribute_group import clean_attributes

        attrs = clean_attributes(attrs)

        aag = cls.write_activity_attribute_group(
            attrs, tag_group, year, name
        )

        comments = cls.get_comments(tag_group)
        if comments:
            aag.attributes.update({
                tag_group.fk_a_tag.fk_a_value.value + '_comment': '\n'.join(comments)
            })

            if cls._save:
                aag.save(using=V2)

    @classmethod
    @lru_cache(maxsize=128, typed=True)
    def matching_activity_id(cls, tag_group):
        if MapActivity.new_class.objects.using(V2).filter(pk=tag_group.fk_activity.pk):
            return tag_group.fk_activity.pk

        activity_identifier = MapActivity.new_class.history.using(V2).filter(
            id=tag_group.fk_activity.pk
        ).values_list(
            'activity_identifier', flat=True
        ).distinct().first()
        current_activity = MapActivity.new_class.objects.using(V2).filter(
            activity_identifier=activity_identifier
        ).values_list('id', flat=True).distinct().first()

        return current_activity

    tag_group_to_attribute_group_ids = {}

    @classmethod
    def write_activity_attribute_group(cls, attrs, tag_group, year, name):
        activity_id = cls.matching_activity_id(tag_group)
        aag = ActivityAttributeGroup(
            fk_activity_id=activity_id, fk_language=Language.objects.get(pk=1),
            date=year_to_date(year), attributes=attrs, name=name
        )
        if cls._save:
            if not cls.is_current_version(tag_group):
                aag = landmatrix.models.ActivityAttributeGroup.history.using(V2).create(
                    id=cls.get_last_id() + 1,
                    history_date=cls.get_history_date(tag_group),
                    fk_activity_id=activity_id, fk_language=Language.objects.get(pk=1),
                    date=year_to_date(year), attributes=attrs, name=name
                )
            else:
                aag.save(using=V2)

        cls.tag_group_to_attribute_group_ids[tag_group.id] = aag.id
        return aag

    @classmethod
    def get_last_id(cls):
        last_id = ActivityAttributeGroup.objects.using(V2).values().aggregate(Max('id'))['id__max']
        return 0 if last_id is None else last_id

    @classmethod
    def get_history_date(cls, tag_group):
        from from_v1.mapping.map_activity import get_activity_versions
        activity = Activity.objects.using(V2).get(pk=cls.matching_activity_id(tag_group))
        versions = list(get_activity_versions(activity))
        for version in versions:
            if version['id'] == activity.id:
                historical_activity = Activity.history.filter(
                    activity_identifier=activity.activity_identifier
                ).filter(id=activity.id).first()
                return historical_activity.history_date
        # no matching version found
        print('taggroup id, activity id:', tag_group.id, activity.id)
        print('versions:', end=' ')
        pprint(versions)

    @classmethod
    def is_current_version(cls, tag_group):
        return tag_group.fk_activity.pk == cls.matching_activity_id(tag_group)

    @classmethod
    def get_comments(cls, tag_group):
        queryset = Comment.objects.using(V1).filter(fk_a_tag_group=tag_group)
        return [comment.comment for comment in queryset]


class MapActivityTagGroup(MapTagGroups, MapActivityTagGroupBase):

    # prevent error if postgres branch of landmatrix 1 is checked out
    if V1 == 'v1_my':
        old_class = A_Tag_Group

        # to migrate latest versions for one activity only
        # tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity').filter(
        #     fk_activity__pk__in=MapActivity.all_ids()
        # ).filter(fk_activity__activity_identifier=11)
        # to migrate a subset of versioned tag groups
        # tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity')[:10000]
        # to migrate all tag groups including old versions
        tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity')
        key_value_lookup = A_Key_Value_Lookup

    @classmethod
    def relevant_tag_sets(cls, tag_group):
        return [
            [tag_group.fk_a_tag],
            A_Tag.objects.using(V1).
                filter(fk_a_tag_group=tag_group).select_related('fk_a_key', 'fk_a_value'),
        ]

    @classmethod
    def migrate_tags(cls, relevant_tags, tag_group):
        attrs = {}
        year = None
        taggroup_name = tag_group.fk_a_tag.fk_a_value.value
        # print(
        #     '\nmigrate_tags',
        #     ["{}: {}".format(tag.fk_a_key.key, tag.fk_a_value.value) for tag in relevant_tags],
        #     "tag group {}: {}".format(tag_group.fk_a_tag.fk_a_key.key, taggroup_name)
        # )
        for tag in relevant_tags:

            key = tag.fk_a_key.key
            value = tag.fk_a_value.value
            year = tag.fk_a_value.year

            if key in attrs and value != attrs[key]:
                cls.write_activity_attribute_group_with_comments(attrs, tag_group, year, taggroup_name)
                attrs = {}

            attrs[key] = value

        if attrs:
            cls.write_activity_attribute_group_with_comments(attrs, tag_group, year, taggroup_name)

    @classmethod
    @transaction.atomic(using=V2)
    def migrate_lookup(cls):
        print('skipping migrate_lookup! reenable it in MapActivityTagGroup!'); return

        records = MapActivity.all_records()
        cls._count = len(records)
        for i, activity in enumerate(records):

            akv_objects = cls.key_value_lookup.objects.using(V1).\
                filter(activity_identifier=activity['activity_identifier'])

            if not akv_objects and activity['fk_status_id'] in (2, 3):
                print('no key-value=lookup entries for activity '+str(activity))
                exit()

            for cached in akv_objects:
                print('CACHED:', cached.activity_identifier, cached.key, cached.value,
                      cached.year, cached.group)
                activity_id = Activity.objects.using(V2).\
                    filter(activity_identifier=cached.activity_identifier).order_by('-id')[:1][0].pk
                attrs = {cached.key: cached.value}
                cls.write_activity_attribute_group(attrs, activity_id, cached.year, cached.group)

            cls._print_status({'id': 0}, i)
