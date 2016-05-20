from .land_observatory_objects.activity import Activity
from .map_lo_model import MapLOModel
from .map_activity import calculate_history_date, get_history_user

import landmatrix.models

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

def map_status_id(id):
    return id


class MapLOActivities(MapLOModel):

    old_class = Activity
    new_class = landmatrix.models.Activity
    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        cls._count = len(ids)
        return Activity.objects.using(cls.DB).filter(pk__in=ids).values()

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
        versions = cls.get_activity_versions(new)
        for i, version in enumerate(versions):
            if not version['id'] == new.id:
                print('version {}:'.format(version['version']), version)
                if save:
                    landmatrix.models.Activity.history.using(V2).create(
                        id=version['id'],
                        activity_identifier=version['activity_identifier'],
                        availability=version['availability'],
                        fk_status_id=version['fk_status_id'],
                        fully_updated=version['fully_updated'],
                        history_date=calculate_history_date(versions, i),
                        history_user=get_history_user(version)
                    )
        print(new)
        if save:
            new.save(using=V2)

    @classmethod
    def get_activity_versions(cls, activity):
        cursor = connections[cls.DB].cursor()
        cursor.execute(
            """SELECT id FROM activities AS a WHERE activity_identifier = '{}'
            ORDER BY version """.format(activity.activity_identifier)
        )
        ids = [id[0] for id in cursor.fetchall()]
        return Activity.objects.using(cls.DB).filter(pk__in=ids).values()


