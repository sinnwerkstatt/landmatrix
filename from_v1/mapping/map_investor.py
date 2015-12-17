from django.utils import timezone

from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from mapping.aux_functions import get_country_id_for_stakeholder
from migrate import V1
from mapping.map_status import MapStatus
from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def get_country_for_primary_investor(pi_id):

    activity_ids = editor.models.Involvement.objects.using(V1).filter(fk_primary_investor=pi_id).values_list('fk_activity', flat=True)
    if not activity_ids or None in activity_ids:
        return None

    max_activity = max(activity_ids)
    stakeholder_ids = list(editor.models.Involvement.objects.using(V1).filter(fk_activity=max_activity).order_by('-investment_ratio').values_list('fk_stakeholder', flat=True))
    while stakeholder_ids:
        stakeholder_with_greatest_investment_ratio = stakeholder_ids.pop(0)

        country = get_country_id_for_stakeholder(stakeholder_with_greatest_investment_ratio)

        if country:
            return landmatrix.models.Country(country)

    return None


def get_now(_):
    return timezone.now()

class MapPrimaryInvestor(MapModel):

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        cls._count = len(ids)
        return cls.old_class.objects.using(V1).filter(pk__in=ids).values()

    @classmethod
    def all_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM primary_investors AS pi
WHERE version = (SELECT MAX(version) FROM primary_investors WHERE primary_investor_identifier = pi.primary_investor_identifier)
ORDER BY primary_investor_identifier
        """)
        return [id[0] for id in cursor.fetchall()]


class MapInvestor(MapPrimaryInvestor):
    old_class = editor.models.PrimaryInvestor
    new_class = landmatrix.models.Investor
    depends = [ MapStatus ]
    attributes = {
        'primary_investor_identifier': 'investor_identifier',
        'id': ('id', ('fk_country', get_country_for_primary_investor), ('timestamp', get_now))
    }
