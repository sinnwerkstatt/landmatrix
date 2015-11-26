from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1
from mapping.map_activity import MapActivity
from mapping.map_stakeholder import MapStakeholder
from mapping.map_primary_investor import MapPrimaryInvestor

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def get_status_for_investor(primary_investor_id):
    investor = editor.models.PrimaryInvestor.objects.using(V1).get(pk=primary_investor_id)
    return investor.fk_status.pk


class MapInvestorActivityInvolvement(MapModel):
    old_class = editor.models.Involvement
    new_class = landmatrix.models.InvestorActivityInvolvement
    attributes = {
        'investment_ratio': 'percentage',
        'fk_primary_investor_id': ('fk_investor_id', ('fk_status_id', get_status_for_investor))
    }
    depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

    @classmethod
    def all_records(cls):
        activity_ids = MapActivity.all_ids()
        primary_investor_ids = MapPrimaryInvestor.all_ids()
        records = cls.old_class.objects.using(V1).\
            filter(fk_activity__in=activity_ids).\
            filter(fk_primary_investor__in=primary_investor_ids).values()
        cls._count = len(records)
        return records
