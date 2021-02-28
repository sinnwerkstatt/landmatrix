from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from apps.landmatrix.models import (
    Deal,
    Country,
    Location,
    Contract,
    DataSource,
    Investor,
    InvestorVentureInvolvement,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Deal.objects.filter(id=9999).delete()
        countries = Country.objects.all()[:4]
        deal = Deal.objects.create(
            id=9999,
            country=Country.objects.get(name="Uganda"),
            intended_size=123.45,
            contract_size=[{"date": "2020", "value": 234.56}],
            production_size=[{"date": "2020", "value": 456.78}],
            land_area_comment="land_area_comment",
            intention_of_investment=[
                {"date": "2016", "value": ["TIMBER_PLANTATION", "INDUSTRY"]}
            ],
            intention_of_investment_comment="intention_of_investment_comment",
            nature_of_deal=["LEASE", "EXPLOITATION_PERMIT"],
            nature_of_deal_comment="nature_of_deal_comment",
            negotiation_status=[
                {"date": "2006", "value": "CONTRACT_SIGNED"},
                {"value": "CONTRACT_CANCELED"},
            ],
            negotiation_status_comment="negotiation_status_comment",
            implementation_status=[
                {"date": "2006", "value": "STARTUP_PHASE"},
                {"value": "PROJECT_ABANDONED"},
            ],
            implementation_status_comment="implementation_status_comment",
            purchase_price=123_456.78,
            purchase_price_currency_id=1,
            purchase_price_type="PER_AREA",
            purchase_price_area=100,
            purchase_price_comment="purchase_price_comment",
            annual_leasing_fee=100.10,
            annual_leasing_fee_currency_id=2,
            annual_leasing_fee_type="PER_HA",
            annual_leasing_fee_area=10,
            annual_leasing_fee_comment="annual_leasing_fee_comment",
            contract_farming=True,
            on_the_lease_state=True,
            on_the_lease=[
                {"area": 20234, "farmers": 160},
                {"date": "2010", "households": 1157},
            ],
            off_the_lease_state=True,
            off_the_lease=[{"area": "2020"}],
            contract_farming_comment="contract_farming_comment",
            # """ Employment """
            total_jobs_created=True,
            total_jobs_planned=3000,
            total_jobs_planned_employees=20000,
            total_jobs_planned_daily_workers=200,
            # total_jobs_current=[
            #     {"date": "2007", "value": "25"},
            #     {"date": "2011", "value": "500"},
            # ],
            # total_jobs_current_employees=[{"value": "900"}],
            # total_jobs_current_daily_workers=[{"value": "6000"}],
            total_jobs_created_comment="total_jobs_created_comment",
            foreign_jobs_created=True,
            foreign_jobs_planned=2,
            foreign_jobs_planned_employees=20000,
            foreign_jobs_planned_daily_workers=200,
            # foreign_jobs_current=[
            #     {"date": "2007", "value": "25"},
            #     {"date": "2011", "value": "500"},
            # ],
            # foreign_jobs_current_employees=[{"value": "900"}],
            # foreign_jobs_current_daily_workers=[{"value": "6000"}],
            foreign_jobs_created_comment="foreign_jobs_created_comment",
            domestic_jobs_created=True,
            domestic_jobs_planned=1000,
            domestic_jobs_planned_employees=20000,
            domestic_jobs_planned_daily_workers=200,
            # domestic_jobs_current=[
            #     {"date": "2007", "value": "25"},
            #     {"date": "2011", "value": "500"},
            # ],
            # domestic_jobs_current_employees=[{"value": "900"}],
            # domestic_jobs_current_daily_workers=[{"value": "6000"}],
            domestic_jobs_created_comment="domestic_jobs_created_comment",
            involved_actors=[
                {
                    "role": "Government / State institutions",
                    "value": "Ayeyarwaddy Development company ",
                }
            ],
            project_name="Sta. Elvira (Martinez) project",
            investment_chain_comment="investment_chain_comment",
            name_of_community=["Thmey commune"],
            name_of_indigenous_people=["Phnong", "Mil"],
            people_affected_comment="people_affected_comment",
            recognition_status=[
                "INDIGENOUS_RIGHTS_RECOGNIZED",
                "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
            ],
            recognition_status_comment="recognition_status_comment",
            community_consultation="NOT_CONSULTED",
            community_consultation_comment="community_consultation_comment",
            community_reaction="CONSENT",
            community_reaction_comment="community_reaction_comment",
            land_conflicts=True,
            land_conflicts_comment="land_conflicts_comment",
            displacement_of_people=True,
            displaced_people=100000,
            displaced_households=30000,
            displaced_people_from_community_land=30,
            displaced_people_within_community_land=100,
            displaced_households_from_fields=23,
            displaced_people_on_completion=5,
            displacement_of_people_comment="displacement_of_people_comment",
            negative_impacts=["SOCIO_ECONOMIC", "EVICTION"],
            negative_impacts_comment="negative_impacts_comment",
            promised_compensation="promised compensation",
            received_compensation="received compensation",
            promised_benefits=["HEALTH", "EDUCATION", "ROADS"],
            promised_benefits_comment="promised_benefits_comment",
            materialized_benefits=["EDUCATION", "ROADS"],
            materialized_benefits_comment="materialized_benefits_comment",
            presence_of_organizations="some organization presence",
            former_land_owner=["STATE", "COMMUNITY"],
            former_land_owner_comment="former_land_owner_comment",
            former_land_use=["SMALLHOLDER_AGRICULTURE", "OTHER"],
            former_land_use_comment="former_land_use_comment",
            former_land_cover=["CROPLAND"],
            former_land_cover_comment="former_land_cover_comment",
            crops=[
                {"value": ["CAW"], "hectares": "695"},
                {"value": ["MAN"], "hectares": "50"},
            ],
            crops_comment="crops_comment",
            animals=[
                {
                    "value": ["SHP", "DCT"],
                    "date": "2010-02-23",
                    "tons": "10000",
                    "hectares": "2000",
                    "percent": "30",
                }
            ],
            animals_comment="animal_comment",
            mineral_resources=[{"value": ["IRO"]}],
            mineral_resources_comment="resources_comment",
            contract_farming_crops=[
                {"value": "14", "current": True, "hectares": "1306"}
            ],
            contract_farming_crops_comment="contract_farming_crops_comment",
            contract_farming_animals=[{"value": "14"}],
            contract_farming_animals_comment="contract_farming_animals_comment",
            has_domestic_use=True,
            domestic_use=50,
            has_export=True,
            export_country1=countries[0],
            export_country1_ratio=20,
            export_country2=countries[1],
            export_country2_ratio=30,
            export_country3=countries[2],
            export_country3_ratio=50,
            use_of_produce_comment="use_of_produce_comment",
            in_country_processing=True,
            in_country_processing_comment="in_country_processing_comment",
            in_country_processing_facilities="in country processing facilities",
            in_country_end_products="in country end products",
            water_extraction_envisaged=True,
            water_extraction_envisaged_comment="water_extraction_envisaged_comment",
            source_of_water_extraction=["GROUNDWATER"],
            source_of_water_extraction_comment="source_of_water_extraction_comment",
            how_much_do_investors_pay_comment="how_much_do_investors_pay_comment",
            water_extraction_amount=23123,
            water_extraction_amount_comment="water_extraction_amount_comment",
            use_of_irrigation_infrastructure=True,
            use_of_irrigation_infrastructure_comment="use_of_irrigation_infrastructure_comment",
            water_footprint="Water footprint",
            gender_related_information="gender related information",
            vggt_applied="PARTIALLY",
            vggt_applied_comment="vggt_applied_comment",
            prai_applied="PARTIALLY",
            prai_applied_comment="prai_applied_comment",
            overall_comment="overall_comment",
            fully_updated=True,
            confidential=True,
            confidential_reason="RESEARCH_IN_PROGRESS",
            confidential_comment="confidential_comment",
            status=2,
            draft_status=1,
        )

        Location.objects.create(
            name="Kreuzberg",
            description="Ich komm aus Kreuzberg, du ***",
            point=Point(13.402981, 52.497216),
            facility_name="Atomwaffen An- und Verkauf",
            level_of_accuracy="COORDINATES",
            comment="Im Keller der Sinnwerkstatt",
            deal=deal,
        )
        Location.objects.create(
            name="Bern",
            description="hat auch nen Bären.",
            point=Point(7.459640, 46.948007),
            facility_name="Bärengraben",
            level_of_accuracy="COORDINATES",
            comment="Achtung, Braunbär.",
            deal=deal,
        )
        Contract.objects.create(
            number="TSC12312",
            date="2020-02-22",
            expiration_date="2021-01-01",
            agreement_duration=1,
            comment="Halt n Vertrag",
            deal=deal,
        )
        Contract.objects.create(
            number="Streng geheim!",
            date="1985-03-11",
            expiration_date="2024-01-01",
            agreement_duration=1,
            comment="geheimer Vertrag",
            deal=deal,
        )

        DataSource.objects.create(
            type="MEDIA_REPORT",
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            file="ricky.pdf",
            file_not_public=False,
            publication_title="Never gonna give you up!",
            date="2009-10-24",
            name="Mr. Astley",
            company="Trolling Inc.",
            email="rick@rolled.com",
            phone="+1234567890",
            includes_in_country_verified_information=True,
            open_land_contracts_id="RRLD000012",
            comment="Rick-rollin' comment",
            deal=deal,
        )
        DataSource.objects.create(
            type="CONTRACT",
            publication_title="Never gonna give you up!",
            date="2012-01-23",
            comment="Rick-rollin' comment",
            deal=deal,
        )
        deal.save()
        print("Adding investor")
        i1 = Investor.objects.create(
            id=666666,
            name="E-Corp.",
            country=countries[3],
            classification="COMMERCIAL_BANK",
            homepage="http://monsanto.com",
            opencorporates="https://opencorporates.org/666",
            comment="Or is it Apple?",
            status=2,
        )

        pi = Investor.objects.create(
            id=777777,
            name="Mom-Corp.",
            country=countries[3],
            classification="GOVERNMENT",
            homepage="https://futurama.com",
            opencorporates="https://opencorporates.org/6666",
            comment="Destroy all humans",
            status=2,
        )
        InvestorVentureInvolvement.objects.create(
            investor=pi, venture=i1, role="PARENT"
        )
        deal.operating_company = i1
        deal.save()

        # operating_company=
        # locations=
        # contracts=
        # datasources=
