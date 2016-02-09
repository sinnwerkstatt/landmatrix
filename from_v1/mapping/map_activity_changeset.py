from mapping.map_model import MapModel
from mapping.map_status import MapStatus
import landmatrix.models
import editor.models
from migrate import V1

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapActivityChangeset(MapModel):
    old_class = editor.models.A_Changeset
    new_class = landmatrix.models.ActivityChangeset
    depends = []

    attributes = {
        'activity': 'fk_activity',
        'comment': 'comment',
        'timestamp': 'timestamp',
        'source': 'source'
    }
