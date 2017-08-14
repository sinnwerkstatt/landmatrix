from operator import itemgetter

from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2
from from_v1.mapping.map_activity import MapActivity
from from_v1.mapping.map_investor import MapInvestor
from from_v1.mapping.aux_functions import get_now

from django.db import connections, models


def get_fk_activity_id(old_activity_id):
    # Get new activity id for old activity id
    activity_identifier = old_editor.models.Activity.objects.using(V1).get(id=old_activity_id).activity_identifier
    new_activity_id = landmatrix.models.Activity.objects.using(V2).get(activity_identifier=activity_identifier).id
    return new_activity_id


def get_status_for_investor(primary_investor_id):
    investor = old_editor.models.PrimaryInvestor.objects.using(V1).get(pk=primary_investor_id)
    return investor.fk_status.pk


class MapInvestorActivityInvolvement(MapModel):
    old_class = old_editor.models.Involvement
    new_class = landmatrix.models.InvestorActivityInvolvement
    attributes = {
        'investment_ratio': 'percentage',
        'fk_activity_id': ('fk_activity_id', get_fk_activity_id),
        'fk_primary_investor_id': ('fk_investor_id', ('fk_status_id', get_status_for_investor), ('timestamp', get_now))
    }
    depends = [ MapActivity, MapInvestor ]

    @classmethod
    def all_records(cls):
        activity_ids = MapActivity.all_ids_by_status()
        investor_ids = MapInvestor.all_ids()
        stakeholder_ids = cls.all_stakeholder_ids()
        stakeholders_condition = models.Q(
            fk_stakeholder__in=stakeholder_ids) | models.Q(
            fk_stakeholder__isnull=True)
        records_with_duplicates = cls.old_class.objects.using(V1).filter(
            fk_activity__in=activity_ids)
        records_with_duplicates = records_with_duplicates.filter(
            stakeholders_condition)
        records_with_duplicates = records_with_duplicates.filter(
            fk_primary_investor__in=investor_ids).values()
        records = {}
        for record in records_with_duplicates:
            latest = cls.latest_involvement_for(record, records_with_duplicates)
            records[latest['id']] = latest

        print('max len relevant involvements:', cls._max_len)
        cls._count = len(records)
        print('num records', cls._count, 'num activities', len(MapActivity.all_ids()))
        return records.values()

    _max_len = 0
    @classmethod
    def latest_involvement_for(cls, record, all_records):
        relevant_involvements = [
            involvement for involvement in all_records
            if involvement['fk_activity_id'] == record['fk_activity_id']
            if involvement['fk_primary_investor_id'] == record['fk_primary_investor_id']
        ]
        if len(relevant_involvements) > cls._max_len:
            cls._max_len = len(relevant_involvements)
        return max(relevant_involvements, key=lambda i: i['id'])

    @classmethod
    def all_stakeholder_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM stakeholders AS s
WHERE version = (SELECT MAX(version) FROM stakeholders WHERE stakeholder_identifier = s.stakeholder_identifier)
ORDER BY stakeholder_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

