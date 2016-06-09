from django.utils import timezone

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
        filtered_stakeholders = lo_stakeholders.exclude(
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
        new.investor_identifier = new.id
        new.name = old.get_tag_value('Name') or ''
        new.fk_country = get_lm_country(
            old.get_tag_value('Country of origin'))
        classification = cls.get_classification(
            old.get_tag_value('Type of Institution') or '')
        new.classification = classification
        new.homepage = old.get_tag_value('Website') or ''
        new.comment = cls.get_comment(old)
        new.fk_status_id = old.fk_status
        new.timestamp = old.timestamp_entry.replace(tzinfo=timezone.utc)

        cls.save_record_history(old, save=save)

        if save:
            new.save(using=V2)

    @classmethod
    def get_classification(cls, classification_text):
        '''
        Maps LO strings to the new model choice field.
        '''
        classification_text = classification_text.lower().strip()
        if classification_text == 'state-owned company':
            classification = '60'
        elif classification_text == 'public investor':
            classification = '20'
        elif classification_text == 'individual entrepreneur':
            classification = '30'
        elif classification_text == 'private company':
            classification = '10'
        elif classification_text == 'investment fund':
            classification = '170'
        elif classification_text == 'semi-state owned':
            classification = '50'
        else:
            classification = '70'  # other

        return classification

    @classmethod
    def get_comment(cls, old_record):
        unmapped_fields = all_fields_that_do_not_match_new_model(old_record)

        comment_lines = [
            'Imported from Land Observatory',
            'UUID: {}'.format(old_record.stakeholder_identifier),
        ]
        comment_lines += [
            '{}: {}'.format(key, value)
            for key, value in unmapped_fields.items()
        ]

        return '\n'.join(comment_lines)

    @classmethod
    def save_record_history(cls, old, save=False):
        previous_timestamp = None

        for version in old.all_versions:
            if version.pk != old.pk:
                version_name = version.get_tag_value('Name') or ''
                version_country = get_lm_country(
                    old.get_tag_value('Country of origin'))
                version_timestamp = version.timestamp_entry.replace(
                    tzinfo=timezone.utc)
                classification = cls.get_classification(
                    version.get_tag_value('Type of Institution') or '')
                homepage = version.get_tag_value('Website') or ''
                comment = cls.get_comment(version)
                history_date = previous_timestamp or timezone.now()
                history_type = '~' if version.version > 1 else '+'
                version_create_kwargs = dict(
                    id=version.pk,
                    investor_identifier=version.pk,
                    name=version_name, fk_country=version_country,
                    fk_status_id=version.fk_status,
                    classification=classification, homepage=homepage,
                    comment=comment, timestamp=version_timestamp,
                    history_date=history_date, history_user=None,
                    history_type=history_type)

                if save:
                    cls.new_class.history.using(V2).create(
                        **version_create_kwargs)

            previous_timestamp = version.timestamp_entry.replace(
                tzinfo=timezone.utc)


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
