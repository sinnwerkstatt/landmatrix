from django.core.management.base import BaseCommand

from apps.landmatrix.models import Deal

from apps.landmatrix.models.deal import DealTopInvestors

x = """
    delete from landmatrix_contract;
    delete from landmatrix_contractversion;
    alter sequence landmatrix_contract_id_seq restart;
    alter sequence landmatrix_contractversion_id_seq restart;

    delete from landmatrix_location;
    delete from landmatrix_locationversion;
    alter sequence landmatrix_location_id_seq restart;
    alter sequence landmatrix_locationversion_id_seq restart;

    delete from landmatrix_datasource;
    delete from landmatrix_datasourceversion;
    alter sequence landmatrix_datasource_id_seq restart;
    alter sequence landmatrix_datasourceversion_id_seq restart;


    delete from landmatrix_deal_top_investors;
    delete from landmatrix_deal;
    delete from landmatrix_dealversion;
    ALTER SEQUENCE landmatrix_deal_id_seq RESTART;
    ALTER SEQUENCE landmatrix_deal_top_investors_id_seq RESTART;
    ALTER SEQUENCE landmatrix_dealversion_id_seq RESTART;


    delete from landmatrix_investorventureinvolvement;
    delete from landmatrix_investorventureinvolvementversion;
    alter sequence landmatrix_investorventureinvolvement_id_seq restart;
    alter sequence landmatrix_investorventureinvolvementversion_id_seq restart;
    delete from landmatrix_investor;
    delete from landmatrix_investorversion;
    alter sequence landmatrix_investor_id_seq restart;
    alter sequence landmatrix_investorversion_id_seq restart;

    delete from landmatrix_revision;
    alter sequence landmatrix_revision_id_seq restart;

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
