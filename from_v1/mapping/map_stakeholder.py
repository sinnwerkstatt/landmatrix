from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1

from mapping.map_status import MapStatus

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapStakeholder(MapModel):
    old_class = editor.models.Stakeholder
    new_class = landmatrix.models.Stakeholder
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
FROM stakeholders AS s
WHERE version = (SELECT MAX(version) FROM stakeholders WHERE stakeholder_identifier = s.stakeholder_identifier)
ORDER BY stakeholder_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

