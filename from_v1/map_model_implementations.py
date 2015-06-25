__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


from map_model import MapModel
import landmatrix.models
import editor.models

class MapLanguage(MapModel):
        old_class = editor.models.Language
        new_class = landmatrix.models.Language

class MapStatus(MapModel):
        old_class = editor.models.Status
        new_class = landmatrix.models.Status

class MapActivity(MapModel):
        old_class = editor.models.Activity
        new_class = landmatrix.models.Activity
        depends = [ MapStatus ]

def year_to_date(year):
        return None if year is None else str(year)+'-01-07'

class MapActivityAttributeGroup(MapModel):
        old_class = editor.models.ActivityAttributeGroup
        new_class = landmatrix.models.ActivityAttributeGroup
        attributes = {
            'activity': 'fk_activity',
            'language': 'fk_language',
            'year': ('date', year_to_date)
        }
        depends = [ MapActivity, MapLanguage ]

class MapStakeholder(MapModel):
        old_class = editor.models.Stakeholder
        new_class = landmatrix.models.Stakeholder
        depends = [ MapStatus ]

class MapStakeholderAttributeGroup(MapModel):
        old_class = editor.models.StakeholderAttributeGroup
        new_class = landmatrix.models.StakeholderAttributeGroup
        attributes = {
            'stakeholder': 'fk_stakeholder',
            'language': 'fk_language',
        }
        depends = [ MapStakeholder, MapLanguage ]

class MapPrimaryInvestor(MapModel):
        old_class = editor.models.PrimaryInvestor
        new_class = landmatrix.models.PrimaryInvestor
        depends = [ MapStatus ]

class MapInvolvement(MapModel):
        old_class = editor.models.Involvement
        new_class = landmatrix.models.Involvement
        depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

class MapRegion(MapModel):
        old_class = editor.models.Region
        new_class = landmatrix.models.Region

class MapCountry(MapModel):
        old_class = editor.models.Country
        new_class = landmatrix.models.Country
        attributes = {
            'region': 'fk_region',
        }
        depends = [ MapRegion ]

class MapBrowseRule(MapModel):
        old_class = editor.models.BrowseRule
        new_class = landmatrix.models.BrowseRule

class MapBrowseCondition(MapModel):
        old_class = editor.models.BrowseCondition
        new_class = landmatrix.models.BrowseCondition
        depends = [ MapBrowseRule ]
