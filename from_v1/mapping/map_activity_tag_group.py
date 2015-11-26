from mapping.map_activity import MapActivity
from mapping.aux_functions import year_to_date
from migrate import V1, V2
from mapping.map_tag_groups import MapTagGroups

from landmatrix.models import Language, Activity, ActivityAttributeGroup
if V1 == 'v1_my':
    from editor.models import A_Tag, A_Tag_Group, A_Key_Value_Lookup, Comment

from django.db import transaction

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapActivityTagGroup(MapTagGroups):

    # prevent error if postgres branch of landmatrix 1 is checked out
    if V1 == 'v1_my':
        old_class = A_Tag_Group
        tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity').filter(
            fk_activity__pk__in=MapActivity.all_ids()
        )
        key_value_lookup = A_Key_Value_Lookup

    @classmethod
    def relevant_tag_sets(cls, tag_group):
        return [
            [tag_group.fk_a_tag],
            A_Tag.objects.using(V1).filter(fk_a_tag_group=tag_group).select_related('fk_a_key', 'fk_a_value'),
        ]

    @classmethod
    def migrate_tags(cls, relevant_tags, tag_group):
        attrs = {}
        year = None
        for tag in relevant_tags:
            key = tag.fk_a_key.key
            value = tag.fk_a_value.value
            year = tag.fk_a_value.year

            if key in attrs:
                cls.write_activity_attribute_group_with_comments(attrs, tag_group, year)
                attrs = {}

            attrs[key] = value

        if attrs:
            cls.write_activity_attribute_group_with_comments(attrs, tag_group, year)

    @classmethod
    def write_activity_attribute_group_with_comments(cls, attrs, tag_group, year):

        aag = cls.write_activity_attribute_group(attrs, tag_group.fk_activity.pk, year)

        comments = cls.get_comments(tag_group)
        if comments:
            aag.attributes.update({
                tag_group.fk_a_tag.fk_a_value.value + '_comment': '\n'.join(comments)
            })
#           print(aag.attributes)
            if cls._save:
                aag.save(using=V2)

    @classmethod
    def write_activity_attribute_group(cls, attrs, activity_id, year=None):

        from mapping.map_activity_attribute_group import clean_crops_and_target_country

        attrs = clean_crops_and_target_country(attrs)

        aag = ActivityAttributeGroup(
            fk_activity_id=activity_id, fk_language=Language.objects.get(pk=1),
            date=year_to_date(year), attributes=attrs, name=attrs.get('name')
        )

        if cls._save:
            aag.save(using=V2)

        return aag

    @classmethod
    def get_comments(cls, tag_group):
        queryset = Comment.objects.using(V1).filter(fk_a_tag_group=tag_group)
        return [comment.comment for comment in queryset]

    @classmethod
    @transaction.atomic(using=V2)
    def migrate_lookup(cls):
        records = MapActivity.all_records()
        cls._count = len(records)
        for i, activity in enumerate(records):

            akv_objects = cls.key_value_lookup.objects.using(V1).filter(activity_identifier=activity['activity_identifier'])

            if not akv_objects and activity['fk_status_id'] in (2, 3):
                print('no key-value=lookup entries for activity '+str(activity))
                exit()

            for cached in akv_objects:
                activity_id = Activity.objects.using(V2).filter(activity_identifier=cached.activity_identifier).order_by('-version')[:1][0].pk
                attrs = {cached.key: cached.value}
                cls.write_activity_attribute_group(attrs, activity_id)

            cls._print_status({'id': 0}, i)
