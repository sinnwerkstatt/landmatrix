from .land_observatory_objects.stakeholder import Stakeholder
from .map_lo_model import MapLOModel
from .map_lo_activities import map_status_id
from migrate import V2

import landmatrix.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapLOStakeholder(MapLOModel):

    old_class = Stakeholder
    new_class = landmatrix.models.Investor
    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }

    @classmethod
    def all_records(cls):
        # TODO: Only the newest versions should be converted
        lo_stakeholders = cls.old_class.objects.using(cls.DB).order_by(
            'stakeholder_identifier', '-version').distinct(
            'stakeholder_identifier')
        existing_names = cls.get_existing_stakeholder_names()
        existing_stakeholder_ids = [
            stakeholder.id for stakeholder in lo_stakeholders
            if stakeholder.get_tag_value('Name') in existing_names
        ]
        filtered_stakeholders = cls.old_class.objects.using(cls.DB).exclude(
            pk__in=existing_stakeholder_ids)

        # This keeps the printed counters correct
        cls._count = filtered_stakeholders.count()

        return filtered_stakeholders.values()

    @classmethod
    def get_existing_stakeholder_names(cls):
        existing_stakeholders = cls.new_class.objects.using(V2).all()
        existing_names = existing_stakeholders.values_list('name', flat=True)

        return set(existing_names)

    @classmethod
    def save_record(cls, new, save):
        old = cls.old_class.objects.using(cls.DB).get(pk=new.id)

        new.investor_identifier = old.stakeholder_identifier
        new.name = old.get_tag_value('Name')
        new.fk_country = get_lm_country(
            old.get_tag_value('Country of origin'))
        new.classification = old.get_tag_value('Type of Institution')
        new.homepage = old.get_tag_value('Website')
        new.comment = all_fields_that_do_not_match_new_model(old)
        new.fk_status_id = old.fk_status
        new.timestamp = old.timestamp_entry

        cls.save_record_history(old, save=save)

        if save:
            new.save(using=V2)

    @classmethod
    def save_record_history(cls, old, save=False):
        previous_timestamp = None

        for version in old.all_versions:
            if version.pk != old.pk:
                version_name = version.get_tag_value('Name')
                version_country = get_lm_country(
                    old.get_tag_value('Country of origin'))
                history_type = '~' if version.version > 1 else '+'
                version_create_kwargs = dict(
                    id=version.pk,
                    investor_identifier=version.stakeholder_identifier,
                    name=version_name, fk_country=version_country,
                    fk_status_id=version.fk_status,
                    timestamp=version.timestamp_entry,
                    history_date=previous_timestamp,
                    history_user=None, history_type=history_type)
                if save:
                    cls.new_class.history.using(V2).create(
                        **version_create_kwargs)
                else:
                    print('history kwargs', version_create_kwargs)
            previous_timestamp = version.timestamp_entry


def get_lm_country(lo_country_name):
    RENAMED_COUNTRIES = {
        'Hong Kong': 'China, Hong Kong Special Administrative Region',
        'Korea, Republic of': 'Republic of Korea',
        'Taiwan, Province of China': '',
        "Korea, Democratic People's Republic of": "Democratic People's Republic of Korea",
        'United States': 'United States of America',
        'Tanzania, United Republic of': 'United Republic of Tanzania',
        'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
    }

    if lo_country_name in RENAMED_COUNTRIES:
        lo_country_name = RENAMED_COUNTRIES[lo_country_name]

    try:
        country = landmatrix.models.Country.objects.get(name=lo_country_name)
    except landmatrix.models.Country.DoesNotExist:
        message = 'Country "{}" does not exist in land matrix DB'.format(
            lo_country_name)
        print(message)
    else:
        return country


def all_fields_that_do_not_match_new_model(stakeholder):
    KNOWN_KEYS = (
        'Country of origin', 'Type of Institution', 'Website', 'Name',
    )
    found_fields = {}
    for group in stakeholder.tag_groups:
        for tag in group.tags:
            if tag.key.key not in KNOWN_KEYS:
                found_fields[tag.key.key] = tag.value.value

    return found_fields
