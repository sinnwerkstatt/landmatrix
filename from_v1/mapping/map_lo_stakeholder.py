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
        # TODO: filter out the Stakeholders that are already in the Land Matrix
        existing_stakeholders = new_class.objects.using(V2).all().
        # Eval straight off to avoid cross db query
        existing_names = list(existing_stakeholders.values('name', flat=True))

        lo_stakeholders = Stakeholder.objects.using(cls.DB).all()
        lo_stakeholder_values = lo_stakeholders.exclude(
            name__in=existing_names).values()

        return lo_stakeholder_values

    @classmethod
    def save_record(cls, new, save):
        old = Stakeholder.objects.using(cls.DB).get(pk=new.id)
        new.investor_identifier = old.stakeholder_identifier
        new.name = old.get_tag_value('Name')
        new.fk_country = lm_country_for_lo_country(old.get_tag_value('Country of origin'))
        new.classification = old.get_tag_value('Type of Institution')
        new.homepage = old.get_tag_value('Website')
        new.comment = all_fields_that_do_not_match_new_model(old)
        new.fk_status_id = old.fk_status
        new.timestamp = old.timestamp_entry

        if save:
            # TODO save older versions as historical records (see map_lo_activities.save_activity_record()
            new.save(using=V2)


def lm_country_for_lo_country(country_name):
    try:
        return landmatrix.models.Country.objects.get(name=country_name)
    except Exception:
        # TODO: some countries have been renamed
        print(country_name, 'does not exist as such in land matrix DB')


def all_fields_that_do_not_match_new_model(stakeholder):
    found_fields = {}
    for group in stakeholder.tag_groups:
        for tag in group.tags:
            if tag.key.key not in ('Country of origin', 'Type of Institution', 'Website', 'Name'):
                found_fields[tag.key.key] = tag.value.value
    return found_fields
