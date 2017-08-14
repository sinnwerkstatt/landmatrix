
from django.utils import timezone

from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.mapping.aux_functions\
    import get_country_id_for_stakeholder
from from_v1.migrate import V1, V2
from from_v1.mapping.map_status import MapStatus
from django.db import connections


def get_country_for_primary_investor(pi_id):
    inv = old_editor.models.Involvement.objects.using(V1).filter(fk_primary_investor_id=pi_id)
    if inv.count() > 0:
        activity = inv[0].fk_activity
        if activity:
            target_country = old_editor.models.A_Key_Value_Lookup.objects.using(V1).filter(activity_identifier=activity.activity_identifier, key="target_country")
            if target_country:
                return landmatrix.models.Country.objects.using(V2).get(id=target_country[0].value)
    return None


def get_now(_):
    return timezone.now()

def get_classification(_):
    return '10'

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
SELECT pi.id
FROM primary_investors AS pi
-- left join involvements i on i.fk_primary_investor = pi.id
-- left join activities a on i.fk_activity = a.id
WHERE pi.version = (SELECT MAX(p.version) FROM primary_investors p WHERE p.primary_investor_identifier = pi.primary_investor_identifier)
-- AND a.activity_identifier = 4948
ORDER BY pi.primary_investor_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

    @classmethod
    def save_record(cls, new, save):
        """Save all versions of an activity as HistoricalActivity records."""
        if not save:
            return

        landmatrix.models.HistoricalInvestor.objects.create(
            id=new.id,
            investor_identifier=new.investor_identifier,
            name=new.name.strip(),
            fk_country=new.fk_country,
            classification=new.classification,
            parent_relation=new.parent_relation,
            homepage=new.homepage,
            opencorporates_link=new.opencorporates_link,
            fk_status=new.fk_status,
            timestamp=new.timestamp,
            comment=new.comment,
            history_date=new.timestamp,
            #history_user=get_history_user(new)
        )
        new.save(using=V2)


class MapInvestor(MapPrimaryInvestor):
    old_class = old_editor.models.PrimaryInvestor
    new_class = landmatrix.models.Investor
    depends = [MapStatus]
    attributes = {
        'id': (
            'id',
            ('fk_country', get_country_for_primary_investor),
            ('timestamp', get_now),
            ('classification', get_classification)
        ),
        'primary_investor_identifier': 'investor_identifier',
        'fk_status': 'fk_status',
        'name': 'name',
    }
