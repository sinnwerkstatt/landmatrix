
from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1

from mapping.map_status import MapStatus

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class MapPrimaryInvestor(MapModel):
    old_class = editor.models.PrimaryInvestor
    new_class = landmatrix.models.PrimaryInvestor
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
FROM primary_investors AS pi
WHERE version = (SELECT MAX(version) FROM primary_investors WHERE primary_investor_identifier = pi.primary_investor_identifier)
ORDER BY primary_investor_identifier
        """)
        return [id[0] for id in cursor.fetchall()]
