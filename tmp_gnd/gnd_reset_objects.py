from django.core.management.base import BaseCommand

from apps.landmatrix.models import Deal

from apps.landmatrix.models.deal import DealTopInvestors

x = """
    -- delete from landmatrix_deal_top_investors;
    -- delete from landmatrix_deal;
    -- delete from landmatrix_dealversion;
    -- ALTER SEQUENCE landmatrix_deal_id_seq RESTART;
    -- ALTER SEQUENCE landmatrix_deal_top_investors_id_seq RESTART;
    -- ALTER SEQUENCE landmatrix_dealversion_id_seq RESTART;
"""
y = """
    delete from landmatrix_investorworkflowinfo;
    alter sequence landmatrix_investorworkflowinfo_id_seq restart;
    delete from landmatrix_investorventureinvolvement;
    alter sequence landmatrix_investorventureinvolvement_id_seq restart;

    -- Investor.objects.all().delete()

    delete from landmatrix_investor;
    delete from landmatrix_investorversion;
    alter sequence landmatrix_investor_id_seq restart;
    alter sequence landmatrix_investorversion_id_seq restart;

    -- ./manage.py sync_investors

    SELECT setval('landmatrix_investor_id_seq', COALESCE((SELECT MAX(id)+1 FROM landmatrix_investor), 1), false);

    -- delete from landmatrix_revision;
    -- alter sequence landmatrix_revision_id_seq restart;

"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Deleting Deal Top Investors")
        DealTopInvestors.objects.all().delete()
        print("Deleting Deals")
        Deal.objects.all().delete()

        # Version.objects.get_for_model(DataSource).delete()
        # Version.objects.get_for_model(Location).delete()
        # Version.objects.get_for_model(Contract).delete()
        # Version.objects.get_for_model(Deal).delete()

        # print("Deleting Involvements")
        # InvestorVentureInvolvement.objects.all().delete()
        # print("Deleting Investors")
        # Investor.objects.all().delete()
        #
        # print("Deleting Versions")
        # Version.objects.all().delete()
        # print("Deleting Revisions")
        # Revision.objects.all().delete()
