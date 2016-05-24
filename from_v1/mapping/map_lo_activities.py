from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Max
from functools import lru_cache

from .land_observatory_objects.tags import A_Value
from .land_observatory_objects.tags import A_Tag
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.tag_groups import A_Tag_Group
from .map_lo_model import MapLOModel
from .map_activity import calculate_history_date, get_history_user
from django.utils import timezone
from migrate import V2

import landmatrix.models

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

def map_status_id(id):
    return id


class MapLOActivities(MapLOModel):

    _save = False

    old_class = Activity
    new_class = landmatrix.models.Activity
    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        # exclude the deals that have been imported from landmatrix and not changed
        # ...

        all_deals = Activity.objects.using(cls.DB).filter(pk__in=ids)
        deals = [
            deal
            for deal in all_deals
            if get_deal_country(deal) not in ['China', 'Myanmar', 'Tanzania', 'Viet Nam']
        ]
        cls._count = len(deals)

        return Activity.objects.using(cls.DB).filter(pk__in=[deal.id for deal in deals]).values()


    @classmethod
    def all_ids(cls):
        cursor = connections[cls.DB].cursor()
        cursor.execute("""
    SELECT id
    FROM activities AS a
    WHERE version = (SELECT MAX(version) FROM activities WHERE activity_identifier = a.activity_identifier)
    ORDER BY activity_identifier
            """)
        return [id[0] for id in cursor.fetchall()]


    @classmethod
    def save_record(cls, new, save):
        """Save all versions of an activity as HistoricalActivity records."""
        cls._save = save
        cls.save_activity_record(new, save)
        tag_groups = A_Tag_Group.objects.using(cls.DB).filter(fk_activity=new.id)

        for tag_group in tag_groups:
            attrs = {}
            taggroup_name = cls.tag_group_name(tag_group)
            # print(
            #     '\nmigrate_tags',
            #     ["{}: {}".format(tag.key.key, tag.value.value) for tag in cls.relevant_tags(tag_group)],
            #     "tag group {}: {}".format(cls.tag_group_key(tag_group), taggroup_name)
            # )
            for tag in cls.relevant_tags(tag_group):

                key = tag.key.key
                value = tag.value.value

                if key in attrs and value != attrs[key]:
                    cls.write_activity_attribute_group_with_comments(attrs, tag_group, None, taggroup_name)
                    attrs = {}

                attrs[key] = value

            if attrs:
                cls.write_activity_attribute_group_with_comments(attrs, tag_group, None, taggroup_name)

    @classmethod
    def tag_group_name(cls, tag_group):
        map_to_name = {
            'Animals': 'crop_animal_mineral',
            'Annual leasing fee area (ha)': 'leasing_fees',
            'Announced amount of investement': '',
            'Announced amount of investment': '',
            'Area (ha)': '',
            'Benefits for local communities': 'community_compensation',
            'Consultation of local community': 'community_reaction',
            'Contract area (ha)': 'contract_farming',
            'Contract date': 'contract_farming',
            'Contract farming': 'contract_farming',
            'Contract Number': 'contract_farming',
            'Country': 'location_1',
            'Crop': 'crop_animal_mineral',
            'Current area in operation (ha)': 'production_size',
            'Current Number of daily/seasonal workers': 'total_number_of_jobs_created',
            'Current number of employees': 'total_number_of_jobs_created',
            'Current total number of jobs': 'total_number_of_jobs_created',
            'Data source': 'data_source_1',
            'Date': '',
            'Duration of Agreement (years)': 'agreement_duration',
            'Files': 'data_source_1',
            'Former predominant land cover': 'land_cover',
            'Former predominant land owner': 'land_owner',
            'Former predominant land use': 'land_use',
            'How did community react': 'community_reaction',
            'How much do investors pay for water': 'water_extraction_amount',
            'How much water is extracted (m3/year)': 'water_extraction_amount',
            'Implementation status': 'implementation_status',
            'Intended area (ha)': 'land_area',
            'Intention of Investment': 'intention',
            'Leasing fee (per year)': 'leasing_fees',
            'Mineral': 'crop_animal_mineral',
            'Name': '',
            'Nature of the deal': 'nature',
            'Negotiation Status': 'negotiation_status',
            'Number of farmers': '',
            'Number of people actually displaced': 'number_of_displaced_people',
            'Original reference number': '',
            'Percentage': '',
            'Planned Number of daily/seasonal workers': 'total_number_of_jobs_created',
            'Planned number of employees': 'total_number_of_jobs_created',
            'Planned total number of jobs': 'total_number_of_jobs_created',
            'Promised or received compensation': 'community_compensation',
            'Purchase price': 'purchase_price',
            'Purchase price area (ha)': 'purchase_price',
            'Remark': 'data_source_1',
            'Scope of agriculture': '',
            'Scope of forestry': '',
            'Spatial Accuracy': 'location_1',
            'URL / Web': 'data_source_1',
            'Use of produce': 'use_of_produce',
            'Water extraction': 'water_extraction_envisaged',
            'Year': '',
        }

        try:
            for key, value in map_to_name.items():
                if key in tag_group.tag.key.key:
                    return value
            print(tag_group, tag_group.tag)
            return A_Value.objects.using(cls.DB).get(pk=tag_group.tag.fk_a_value).value
        except Exception:
            return None

    @classmethod
    def tag_group_key(cls, tag_group):
        try:
            return tag_group.tag.key.key
        except Exception:
            return None

    @classmethod
    def relevant_tags(cls, tag_group):
        return tag_group.tags

    @classmethod
    def write_activity_attribute_group_with_comments(cls, attrs, tag_group, year, name):
        if (len(attrs) == 1) and attrs.get('name'):
            return

        attrs = clean_attributes(attrs)
        aag = cls.write_activity_attribute_group(
            attrs, tag_group, year, name
        )

    @classmethod
    def write_activity_attribute_group(cls, attrs, tag_group, year, name):
        activity_id = cls.matching_activity_id(tag_group)
        if 'YEAR' in attrs:
            year = attrs['YEAR']
            del attrs['YEAR']
        aag = landmatrix.models.ActivityAttributeGroup(
            fk_activity_id=activity_id, fk_language=landmatrix.models.Language.objects.get(pk=1),
            date=year, attributes=attrs, name=name
        )
        if cls._save:
            if not cls.is_current_version(tag_group):
                aag = landmatrix.models.ActivityAttributeGroup.history.using(V2).create(
                    id=cls.get_last_id() + 1,
                    history_date=cls.get_history_date(tag_group),
                    fk_activity_id=activity_id, fk_language=landmatrix.models.Language.objects.get(pk=1),
                    date=year, attributes=attrs, name=name
                )
            else:
                aag.save(using=V2)
        else:
            print(aag)

        cls.tag_group_to_attribute_group_ids[tag_group.id] = aag.id
        return aag

    @classmethod
    def is_current_version(cls, tag_group):
        return tag_group.fk_activity == cls.matching_activity_id(tag_group)

    @classmethod
    @lru_cache(maxsize=128, typed=True)
    def matching_activity_id(cls, tag_group):
        if landmatrix.models.Activity.objects.using(V2).filter(pk=tag_group.fk_activity):
            return tag_group.fk_activity

        activity_identifier = landmatrix.models.Activity.history.using(V2).filter(
            id=tag_group.fk_activity
        ).values_list(
            'activity_identifier', flat=True
        ).distinct().first()
        current_activity = landmatrix.models.Activity.objects.using(V2).filter(
            activity_identifier=activity_identifier
        ).values_list('id', flat=True).distinct().first()

        return current_activity

    tag_group_to_attribute_group_ids = {}

    @classmethod
    def save_activity_record(cls, new, save):
        activity_identifier = cls.get_deal_id(new)
        versions = cls.get_activity_versions(new)
        for i, version in enumerate(versions):
            if not version['id'] == new.id:
                if save:
                    landmatrix.models.Activity.history.using(V2).create(
                        id=version['id'],
                        activity_identifier=activity_identifier,
                        availability=version['reliability'],
                        fk_status_id=version['fk_status'],
                        fully_updated=None,
                        history_date=calculate_history_date(versions, i),
                        history_user=get_history_user(version)
                    )
        if save:
            new.activity_identifier = activity_identifier
            new.save(using=V2)

    @classmethod
    def get_deal_id(cls, activity):
        # if activity already in DB, return its ID
        return landmatrix.models.Activity.objects.using(V2).values().\
            aggregate(Max('activity_identifier'))['activity_identifier__max']+1

    @classmethod
    def get_activity_versions(cls, activity):
        cursor = connections[cls.DB].cursor()
        cursor.execute(
            """SELECT id FROM activities AS a WHERE activity_identifier = '{}'
            ORDER BY version """.format(activity.activity_identifier)
        )
        ids = [id[0] for id in cursor.fetchall()]
        return Activity.objects.using(cls.DB).filter(pk__in=ids).values()


def clean_attributes(attrs):
    attrs = {
        clean_key(key): clean_attribute(key, value) for key, value in attrs.items()
    }


    return attrs


def clean_attribute(key, value):
    if isinstance(value, str):
        return value[:3000]


def clean_key(key):
    return LM_ATTRIBUTES.get(key, key)


LM_ATTRIBUTES = {
    'Animals':                          'animals',
    'Annual leasing fee area (ha)':     'annual_leasing_fee_area',
    'Announced amount of investement':  'ANNOUNCED_AMOUNT_OF_INVESTMENT',
    'Announced amount of investment':   'ANNOUNCED_AMOUNT_OF_INVESTMENT',
    'Area (ha)':                        'AREA',
    'Benefits for local communities':   'promised_benefits',
    'Consultation of local community':  'community_consultation',
    'Contract area (ha)':               'contract_size',
    'Contract date':                    'contract_date',
    'Contract farming':                 'contract_farming',
    'Contract Number':                  'contract_number',
    'Country':                          'target_country',
    'Crop':                             'crops',
    'Current area in operation (ha)':   'production_size',
    'Current Number of daily/seasonal workers': 'total_jobs_current_daily_workers',
    'Current number of employees':      'total_jobs_current_employees',
    'Current total number of jobs':     'total_jobs_current',
    'Data source':                      'data_source',
    'Date':                             'date',
    'Duration of Agreement (years)':    'agreement_duration',
    'Files':                            'file',
    'Former predominant land cover':    'land_cover',
    'Former predominant land owner':    'land_owner',
    'Former predominant land use':      'land_use',
    'How did community react':          'community_reaction',
    'How much do investors pay for water': 'how_much_do_investors_pay_comment',
    'How much water is extracted (m3/year)': 'water_extraction_amount',
    'Implementation status':            'implementation_status',
    'Intended area (ha)':               'INTENDED_AREA',
    'Intention of Investment':          'intention',
    'Leasing fee (per year)':           'annual_leasing_fee',
    'Mineral':                          'minerals',
    'Name':                             'NAME',
    'Nature of the deal':               'nature',
    'Negotiation Status':               'negotiation_status',
    'Number of farmers':                'NUMBER_OF_FARMERS',
    'Number of people actually displaced': 'number_of_displaced_people',
    'Original reference number':        'ORIGINAL_REFERENCE_NUMBER',
    'Percentage':                       'PERCENTAGE',
    'Planned Number of daily/seasonal workers': 'total_jobs_planned_daily_workers',
    'Planned number of employees':      'total_jobs_planned_employees',
    'Planned total number of jobs':     'total_jobs_planned',
    'Promised or received compensation': 'promised_compensation',
    'Purchase price':                   'purchase_price',
    'Purchase price area (ha)':         'purchase_price_area',
    'Remark':                           'REMARK',
    'Scope of agriculture':             'SCOPE_OF_AGRICULTURE',
    'Scope of forestry':                'SCOPE_OF_FORESTRY',
    'Spatial Accuracy':                 'level_of_accuracy',
    'URL / Web':                        'url',
    'Use of produce':                   'use_of_produce_comment',
    'Water extraction':                 'water_extraction_envisaged',
    'Year':                             'YEAR',
}


def get_deal_country(deal):
    for group in deal.tag_groups:
        for tag in group.tags:
            if tag.key.key == 'Country':
                return tag.value.value
