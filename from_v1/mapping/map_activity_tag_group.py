import re
from pprint import pprint

from django.db.models.aggregates import Max
from functools import lru_cache
from from_v1.mapping.map_activity import MapActivity
from from_v1.mapping.aux_functions import year_to_date
from from_v1.migrate import V1, V2
from from_v1.mapping.map_tag_groups import MapTagGroups

from landmatrix.models.language import Language
from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup, ActivityAttribute, HistoricalActivityAttribute

if V1 == 'v1_my':
    from old_editor.models import A_Tag, A_Tag_Group, A_Key_Value_Lookup, Comment

from django.db import transaction



class MapActivityTagGroupBase:

    YEAR_BASED_DATA_SEPARATOR = '#'

#    @classmethod
#    def write_activity_attribute_group_with_comments(cls, attrs, tag_group, year, name):
#        if (len(attrs) == 1) and attrs.get('name'):
#            return
#
#        from from_v1.mapping.map_activity_attribute_group import clean_attributes
#
#        attrs = clean_attributes(attrs)
#
#        aag = cls.write_activity_attribute_group(
#            attrs, tag_group, year, name
#        )
#
#        comments = cls.get_comments(tag_group)
#        if comments:
#            aag.attributes.update({
#                tag_group.fk_a_tag.fk_a_value.value + '_comment': '\n'.join(comments)
#            })
#
#            if cls._save:
#                aag.save(using=V2)

    @classmethod
    @lru_cache(maxsize=128, typed=True)
    def matching_activity_id(cls, tag_group):
        if Activity.objects.filter(pk=tag_group.fk_activity).count() > 0:
            return tag_group.fk_activity

        activity_identifier = Activity.objects.filter(
            id=tag_group.fk_activity
        ).values_list(
            'activity_identifier', flat=True
        ).distinct().first()
        current_activity = Activity.objects.filter(
            activity_identifier=activity_identifier
        ).values_list('id', flat=True).distinct().first()

        return current_activity

    tag_group_to_attribute_group_ids = {}

    #@classmethod
    #def get_last_id(cls):
    #    last_id = ActivityAttributeGroup.objects.using(V2).values().aggregate(Max('id'))['id__max']
    #    return 0 if last_id is None else last_id

    @classmethod
    def get_history_date(cls, tag_group):
        from from_v1.mapping.map_activity import get_activity_versions
        activity = Activity.objects.using(V2).get(pk=cls.matching_activity_id(tag_group))
        versions = list(get_activity_versions(activity))
        for version in versions:
            if version['id'] == activity.id:
                historical_activity = HistoricalActivity.objects.filter(
                    activity_identifier=activity.activity_identifier
                ).filter(id=activity.id).first()
                return historical_activity.history_date
        # no matching version found
        print('group id, activity id:', tag_group.id, activity.id)
        print('versions:', end=' ')
        pprint(versions)

    @classmethod
    def is_current_version(cls, tag_group):
        return Activity.objects.filter(pk=tag_group.fk_activity.pk).count() > 0
        #return tag_group.fk_activity.pk == cls.matching_activity_id(tag_group)

    #@classmethod
    #def get_comments(cls, tag_group):
    #    queryset = Comment.objects.using(V1).filter(fk_a_tag_group=tag_group)
    #    return [comment.comment for comment in queryset]


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
        tag_groups = A_Tag_Group.objects.using(V1).select_related('fk_activity')#.filter(fk_activity__activity_identifier=4948)
        #key_value_lookup = A_Key_Value_Lookup

    #@classmethod
    #def relevant_tag_sets(cls, tag_group):
    #    return [
    #        [tag_group.fk_a_tag],
    #        A_Tag.objects.using(V1).
    #            filter(fk_a_tag_group=tag_group).select_related('fk_a_key', 'fk_a_value'),
    #    ]

    @classmethod
    def migrate_tag_group(cls, tag_group):
        from from_v1.mapping.map_activity_attribute_group import clean_attribute, clean_group
        tg_name = tag_group.fk_a_tag.fk_a_value.value

        activity_id = tag_group.fk_activity.id#cls.matching_activity_id(tag_group)
        #raise IOError(activity_id)
        aag, created = ActivityAttributeGroup.objects.get_or_create(
            name=clean_group(tg_name, None, None)
        )
        if cls._save:
            aag.save(using=V2)
        is_current = cls.is_current_version(tag_group)

        attributes = {}
        old_values = {}
        for tg in A_Tag_Group.objects.using(V1).filter(fk_activity=activity_id):
            for tag in tg.a_tag_set.all():
                key = tag.fk_a_key.key
                value = tag.fk_a_value.value
                if key in old_values:
                    old_values[key].append(value)
                else:
                    old_values[key] = [value]
        for tag in tag_group.a_tag_set.all():
            key = tag.fk_a_key.key
            value = tag.fk_a_value.value
            year = tag.fk_a_value.year
            #if year:
            #    year = year_to_date(year)
            key, value = clean_attribute(key, value, old_values=old_values)
            if not key or not value:
                continue
            tag_aag = clean_group(tg_name, key, value)
            if tag_aag != aag.name:
                tag_aag, created = ActivityAttributeGroup.objects.get_or_create(
                    name=tag_aag
                )
                if cls._save:
                    tag_aag.save(using=V2)
            else:
                tag_aag = aag
            if is_current:
                aa = ActivityAttribute(
                    fk_activity_id=activity_id,
                    fk_language_id=1,
                    fk_group=tag_aag,
                    name=key,
                    value=value,
                    date=year or None,
                )
                if cls._save:
                    aa.save(using=V2)
            aa = HistoricalActivityAttribute(
                #id=cls.get_last_id() + 1,
                fk_activity_id=activity_id,
                fk_language_id=1,
                fk_group=tag_aag,
                name=key,
                value=value,
                date=year or None,
            )
            if cls._save:
                aa.save(using=V2)

            if key in attributes:
                attributes[key]['values'].append(value)
            else:
                attributes[key] = dict(fk_group=tag_aag, year=year, values=[value])

        if 'intention' in attributes and len(attributes['intention']['values']) == 1:
            value = None
            if attributes['intention']['values'][0] == 'Agriculture':
                value = 'Agriculture unspecified'
            elif attributes['intention']['values'][0] == 'Forestry':
                value = 'Forestry unspecified'
            if value:
                intention = attributes['intention']
                if is_current:
                    aa = ActivityAttribute(
                        fk_activity_id=activity_id,
                        fk_language_id=1,
                        fk_group=intention['fk_group'],
                        name='intention',
                        value=value,
                        date=intention['year'] or None,
                    )
                    if cls._save:
                        aa.save(using=V2)
                aa = HistoricalActivityAttribute(
                    # id=cls.get_last_id() + 1,
                    fk_activity_id=activity_id,
                    fk_language_id=1,
                    fk_group=intention['fk_group'],
                    name='intention',
                    value=value,
                    date=intention['year'] or None,
                )
                if cls._save:
                    aa.save(using=V2)
        if 'For wood and fibre' in old_values.get('intention', []):
            if 'True' in  old_values.get('not_public', []) or 'Exploitation license' in old_values.get('nature', []):
                tag_aag, created = ActivityAttributeGroup.objects.get_or_create(
                    name='intention'
                )
                if is_current:
                    aa = ActivityAttribute(
                        fk_activity_id=activity_id,
                        fk_language_id=1,
                        fk_group=tag_aag.id,
                        name='intention',
                        value='Concession',
                        date=None,
                    )
                    if cls._save:
                        aa.save(using=V2)
                aa = HistoricalActivityAttribute(
                    # id=cls.get_last_id() + 1,
                    fk_activity_id=activity_id,
                    fk_language_id=1,
                    fk_group=tag_aag.id,
                    name='intention',
                    value='Concession',
                    date=None,
                )
                if cls._save:
                    aa.save(using=V2)


        for comment in tag_group.comment_set.all():
            key = 'tg_%s_comment' % re.sub('_\d+', '', tg_name)
            key, value = clean_attribute(key, comment.comment)
            if is_current:
                aa = ActivityAttribute(
                    fk_activity_id=activity_id,
                    fk_language_id=1,
                    fk_group=aag,
                    name=key,
                    value=value,
                )
                if cls._save:
                    aa.save(using=V2)
            aa = HistoricalActivityAttribute(
                fk_activity_id=activity_id,
                fk_language_id=1,
                fk_group=aag,
                name=key,
                value=value,
            )
            if cls._save:
                aa.save(using=V2)
            #cls.tag_group_to_attribute_group_ids[tag_group.id] = aag.id
    

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
                activity_id = HistoricalActivity.objects.using(V2).\
                    filter(activity_identifier=cached.activity_identifier).order_by('-id')[:1][0].pk
                attrs = {cached.key: cached.value}
                cls.write_activity_attribute_group(attrs, activity_id, cached.year, cached.group)

            cls._print_status({'id': 0}, i)