from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1
from mapping.map_activity import MapActivity
#from mapping.map_stakeholder import MapStakeholder

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


# class MapInvolvement(MapModel):
#     old_class = editor.models.Involvement
#     new_class = landmatrix.models.Involvement
#     depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]
#
#     @classmethod
