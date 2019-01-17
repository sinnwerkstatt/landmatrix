from from_v1.mapping.map_stakeholder_tag_group import MapStakeholderTagGroup
import landmatrix.models
import editor.models
from from_v1.mapping.map_model import MapModel
from from_v1.migrate import V1
from from_v1.mapping.map_stakeholder import MapStakeholder
from from_v1.mapping.map_language import MapLanguage
from from_v1.mapping.aux_functions import replace_country_name_with_id
from grid.views.activity_protocol import ActivityProtocol


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
