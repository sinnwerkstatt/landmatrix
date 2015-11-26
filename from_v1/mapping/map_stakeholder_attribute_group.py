from mapping.map_stakeholder_tag_group import MapStakeholderTagGroup
import landmatrix.models
import editor.models
from mapping.map_model import MapModel
from migrate import V1
from mapping.map_stakeholder import MapStakeholder
from mapping.map_language import MapLanguage
from mapping.aux_functions import replace_country_name_with_id

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def clean_country(attributes):
    return replace_country_name_with_id(attributes, 'country')

if V1 == 'v1_pg':
    class MapStakeholderAttributeGroup(MapModel):
        old_class = editor.models.StakeholderAttributeGroup
        new_class = landmatrix.models.StakeholderAttributeGroup
        attributes = {
            'stakeholder': 'fk_stakeholder',
            'language': 'fk_language',
            'attributes': ('attributes', clean_country)
        }
        depends = [ MapStakeholder, MapLanguage ]
else:
    MapStakeholderAttributeGroup = MapStakeholderTagGroup

