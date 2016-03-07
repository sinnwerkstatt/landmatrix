from mapping.map_model import MapModel
from mapping.map_status import MapStatus
import landmatrix.models
import old_editor.models
from migrate import V1

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapActivity(MapModel):
    old_class = old_editor.models.Activity
    new_class = landmatrix.models.Activity
    depends = [ MapStatus ]

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
FROM activities AS a
WHERE version = (SELECT MAX(version) FROM activities WHERE activity_identifier = a.activity_identifier)
ORDER BY activity_identifier
        """)
        return [id[0] for id in cursor.fetchall()]
