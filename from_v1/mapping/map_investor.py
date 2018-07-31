from django.utils import timezone

from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2
from from_v1.mapping.map_status import MapStatus
from django.db import connections
from django.contrib.auth.models import User


def get_country_for_primary_investor(pi_id):
    invs = old_editor.models.Involvement.objects.using(V1).filter(fk_primary_investor_id=pi_id)
    for inv in invs:
        activity = inv.fk_activity
        if activity:
            target_country = old_editor.models.A_Key_Value_Lookup.objects.using(V1).filter(activity_identifier=activity.activity_identifier, key="target_country")
            if target_country:
                return landmatrix.models.Country.objects.using(V2).get(id=target_country[0].value)
    return None


def get_now(_):
    return timezone.now()


def get_classification(_):
    return '10'


def get_history_data(record):
    changeset = old_editor.models.SH_Changeset.objects.using(V1)
    changeset = changeset.filter(fk_stakeholder_id=record['id']).last()
    history_user_id = None
    if changeset:
        history_date = changeset.timestamp
        if User.objects.filter(id=changeset.fk_user_id).count() > 0:
            history_user_id = changeset.fk_user_id
    else:
        history_date = get_now(record['id'])
    return history_date, history_user_id


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

        versions = get_primary_investor_versions(new)
        for i, version in enumerate(versions):
            history_date, history_user_id = get_history_data(version)
            landmatrix.models.HistoricalInvestor.objects.create(
                id=version['id'],
                investor_identifier=version['primary_investor_identifier'],
                name=version['name'].strip(),
                fk_country=get_country_for_primary_investor(version['id']),
                classification=get_classification(version['id']),
                fk_status_id=version['fk_status_id'],
                history_date=history_date,
                history_user_id=history_user_id,
                #parent_relation=version['parent_relation'],
                #homepage=version['homepage'],
                #opencorporates_link=version['opencorporates_link'],
                #comment=version['comment'],
                #history_date=version['timestamp'],
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
            ('classification', get_classification),
        ),
        'primary_investor_identifier': 'investor_identifier',
        'fk_status': 'fk_status',
        'name': 'name',
    }


def get_primary_investor_versions(investor):
    return MapInvestor.old_class.objects.using(V1).filter(
        primary_investor_identifier=investor.investor_identifier).order_by(
        'version').values()
