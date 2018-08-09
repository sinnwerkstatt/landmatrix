from from_v1.mapping.map_investor_activity_involvement import MapInvestorActivityInvolvement
from from_v1.mapping.map_activity import MapActivity
from from_v1.mapping.map_investor import MapPrimaryInvestor
from from_v1.mapping.map_stakeholder_investor import MapStakeholderInvestor, get_stakeholder_id
from from_v1.mapping.aux_functions import stakeholder_ids
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2
from from_v1.mapping.aux_functions import get_now


def get_venture_for_primary_investor(involvement):
    #landmatrix.models.Investor.objects.using(V2).get(pk=involvement['fk_primary_investor_id'])
    return involvement['fk_primary_investor_id']


def get_stakeholder_id_for_stakeholder(involvement):
    stakeholder_id = get_stakeholder_id(involvement['fk_stakeholder_id'])
    #landmatrix.models.Investor.objects.using(V2).get(pk=stakeholder_id)
    return stakeholder_id


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
            filter(fk_primary_investor__in=primary_investor_ids). \
            filter(fk_stakeholder__in=stakeholder_ids()).values()
        return records

    @classmethod
    def migrate(cls, involvements):
        missing_investors = 0
        for i, involvement in enumerate(involvements):
            fk_venture_id = get_venture_for_primary_investor(involvement)
            fk_investor_id = get_stakeholder_id_for_stakeholder(involvement)
            fk_status_id = get_status(involvement)
            percentage = get_percentage(involvement)
            inv, created = landmatrix.models.InvestorVentureInvolvement.objects.get_or_create(
                fk_investor_id=fk_investor_id,
                fk_venture_id=fk_venture_id,
                role='ST',
            )
            if percentage:
                inv.percentage = percentage
            inv.fk_status_id = fk_status_id
            inv.save()

            versions = get_ivinvolvement_versions(inv)
            for j, version in enumerate(versions):
                hinv, created = landmatrix.models.HistoricalInvestorVentureInvolvement.objects\
                    .get_or_create(
                    fk_venture_id=get_venture_for_primary_investor(version),
                    fk_investor_id=get_stakeholder_id_for_stakeholder(version),
                    role='ST',
                )
                percentage = get_percentage(version)
                if percentage:
                    hinv.percentage = percentage
                hinv.fk_status_id = get_status(version)
                #hinv.history_date = get_now(version['id'])
                hinv.save()
                #investment_type=version['investment_type']
                #loans_amount=version['loans_amount']
                #loans_currency=version['loans_currency']
                #loans_date=version['loans_date']
                #comment=version['comment']

            cls._print_status(involvement, i)

    @classmethod
    def all_records(cls):
        return cls.old_class.objects.using(cls.DB).filter(
            fk_primary_investor_id__in=MapPrimaryInvestor.all_ids(),
            fk_stakeholder_id__in=MapStakeholderInvestor.all_ids()
        ).values()


def get_ivinvolvement_versions(inv):
    return MapStakeholderVentureInvolvement.old_class.objects.using(V1).filter(
        fk_primary_investor__primary_investor_identifier=inv.fk_venture.investor_identifier,
        #fk_stakeholder__stakeholder_identifier=inv.fk_investor.investor_identifier
        fk_stakeholder__isnull=False
    ).order_by('id').values()
