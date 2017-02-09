from mapping.map_investor_activity_involvement import MapInvestorActivityInvolvement
from mapping.map_activity import MapActivity
from mapping.map_investor import MapPrimaryInvestor
from mapping.aux_functions import stakeholder_ids
import landmatrix.models
import old_editor.models
#from mapping.map_involvement import MapInvolvement
from migrate import V1, V2

from datetime import datetime



def get_venture_for_primary_investor(involvement):
    landmatrix.models.Investor.objects.using(V2).get(pk=involvement['fk_primary_investor_id'])
    return involvement['fk_primary_investor_id']


def get_stakeholder_id_for_stakeholder(involvement):
    landmatrix.models.Investor.objects.using(V2).get(pk=involvement['fk_stakeholder_id'])
    return involvement['fk_stakeholder_id']


def get_percentage(involvement):
    return involvement['investment_ratio'] if involvement['investment_ratio'] else None


def get_collective_status(pi_status, st_status):
    if pi_status == st_status:
        return pi_status

    if 1 in (pi_status, st_status): return 1
    if 4 in (pi_status, st_status): return 4
    if 5 in (pi_status, st_status): return 5
    if 6 in (pi_status, st_status): return 6
    return 3


def get_status(involvement):
    pi_status = old_editor.models.PrimaryInvestor.objects.using(V1).get(pk=involvement['fk_primary_investor_id']).fk_status_id
    st_status = old_editor.models.Stakeholder.objects.using(V1).get(pk=involvement['fk_stakeholder_id']).fk_status_id
    return get_collective_status(pi_status, st_status)


class MapStakeholderVentureInvolvement(MapInvestorActivityInvolvement):

    old_class = old_editor.models.Involvement
    new_class = landmatrix.models.InvestorActivityInvolvement

    @classmethod
    def map_all(cls, save=False, verbose=False):

        cls._check_dependencies()
        cls._start_timer()
        cls._save = save

        # migrate original values. in case of conflict, original values overwrite cached values.
        involvements = cls.all_involvements()
        cls._count = len(involvements)
        cls.migrate(involvements)

        cls._done = True
        cls._print_summary()

    @classmethod
    def all_involvements(cls):
        activity_ids = MapActivity.all_ids()

        primary_investor_ids = MapPrimaryInvestor.all_ids()
        records = cls.old_class.objects.using(V1). \
            filter(fk_activity__in=activity_ids). \
            filter(fk_primary_investor__in=primary_investor_ids). \
            filter(fk_stakeholder__in=stakeholder_ids()).values()
        return records

    @classmethod
    def migrate(cls, involvements):
        for i, involvement in enumerate(involvements):
            fk_venture_id = get_venture_for_primary_investor(involvement)
            fk_investor_id = get_stakeholder_id_for_stakeholder(involvement)
            fk_status_id = get_status(involvement)
            percentage = get_percentage(involvement)
            stakeholder_venture_involvement = landmatrix.models.InvestorVentureInvolvement.objects.get_or_create(
                fk_investor_id=fk_investor_id,
                fk_venture_id=fk_venture_id,
                fk_status_id=fk_status_id,
                percentage=percentage,
                role='ST',
            )

            #if cls._save:
            #    stakeholder_venture_involvement.save(using=V2)

            cls._print_status(involvement, i)
