from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import Deal


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO
        error_deals = [
            6859,
            7824,
            7825,
            7826,
            7862,
            8037,
            8166,
            8705,
            8743,
            8746,
            8748,
            8755,
            8974,
            9016,
            9133,
            9140,
            9166,
            9270,
            9274,
            9398,  # purchase_price_area off
            9422,
            9813,
            9843,
            9847,
            9850,
            9858,
            9905,
        ]

        for deal in (
            Deal.objects.prefetch_related("country")
            .exclude(id__in=error_deals)
            .filter(status=1)
            .order_by("id")
        ):
            latest_version = deal.versions.order_by("-id")[0]
            ov = latest_version.serialized_data

            print(deal, latest_version)
            assert ov["status"] == 1
            assert ov["draft_status"] is not None

            # print(deal.confidential, ov["confidential"])
            # assert deal.confidential == ov["confidential"]
            #
            # continue

            # print(deal.locations, ov["locations"])
            # assert deal.locations == ov["locations"]

            print(deal.country_id, ov["country"])
            assert deal.country_id == ov["country"]
            if deal.intended_size or ov["intended_size"]:
                print(type(deal.intended_size))
                print(deal.intended_size, ov["intended_size"])
                # getcontext().prec = 2
                assert round(float(deal.intended_size), 2) == round(
                    float(ov["intended_size"]), 2
                )
                # or float(deal.intended_size) == float(ov["intended_size"])
            if deal.contract_size or ov["contract_size"]:
                print(deal.contract_size, ov["contract_size"])
                assert deal.contract_size == ov["contract_size"]
            assert deal.production_size == ov["production_size"]
            print(deal.land_area_comment, "X", ov["land_area_comment"])
            assert deal.land_area_comment == ov["land_area_comment"]
            assert deal.intention_of_investment == ov["intention_of_investment"]
            assert (
                deal.intention_of_investment_comment
                == ov["intention_of_investment_comment"]
            )
            assert deal.nature_of_deal == ov["nature_of_deal"]
            assert deal.nature_of_deal_comment == ov["nature_of_deal_comment"]
            assert deal.negotiation_status == ov["negotiation_status"]
            assert deal.negotiation_status_comment == ov["negotiation_status_comment"]
            assert deal.implementation_status == ov["implementation_status"]
            assert (
                deal.implementation_status_comment
                == ov["implementation_status_comment"]
            )
            if deal.purchase_price or ov["purchase_price"]:
                assert round(float(deal.purchase_price), 2) == round(
                    float(ov["purchase_price"]), 2
                )

            if deal.purchase_price_currency_id or ov["purchase_price_currency"]:
                assert deal.purchase_price_currency_id == int(
                    ov["purchase_price_currency"]
                )
            assert deal.purchase_price_type == ov["purchase_price_type"]
            if deal.purchase_price_area or ov["purchase_price_area"]:
                print(deal.purchase_price_area, int(ov["purchase_price_area"]))
                assert int(deal.purchase_price_area) == int(ov["purchase_price_area"])
            assert deal.purchase_price_comment == ov["purchase_price_comment"]
            if deal.annual_leasing_fee or ov["annual_leasing_fee"]:
                print(deal.annual_leasing_fee, ov["annual_leasing_fee"])
                assert round(float(deal.annual_leasing_fee), 2) == round(
                    float(ov["annual_leasing_fee"]), 2
                )
            if deal.annual_leasing_fee_currency_id or ov["annual_leasing_fee_currency"]:
                print(
                    deal.annual_leasing_fee_currency_id,
                    ov["annual_leasing_fee_currency"],
                )
                assert deal.annual_leasing_fee_currency_id == int(
                    ov["annual_leasing_fee_currency"]
                )
            assert deal.annual_leasing_fee_type == ov["annual_leasing_fee_type"]
            if deal.annual_leasing_fee_area or ov["annual_leasing_fee_area"]:
                print(deal.annual_leasing_fee_area, ov["annual_leasing_fee_area"])
                assert deal.annual_leasing_fee_area == int(
                    ov["annual_leasing_fee_area"]
                )
            print(deal.annual_leasing_fee_comment, ov["annual_leasing_fee_comment"])
            assert deal.annual_leasing_fee_comment == ov["annual_leasing_fee_comment"]
            assert deal.contract_farming == ov["contract_farming"]
            assert deal.on_the_lease_state == ov["on_the_lease_state"]
            assert deal.on_the_lease == ov["on_the_lease"]
            assert deal.off_the_lease_state == ov["off_the_lease_state"]
            assert deal.off_the_lease == ov["off_the_lease"]
            assert deal.contract_farming_comment == ov["contract_farming_comment"]
            # assert deal.contracts == ov["contracts"]
            assert deal.total_jobs_created == ov["total_jobs_created"]
            if deal.total_jobs_planned or ov["total_jobs_planned"]:
                assert deal.total_jobs_planned == int(ov["total_jobs_planned"])
            if deal.total_jobs_planned_employees or ov["total_jobs_planned_employees"]:
                assert deal.total_jobs_planned_employees == int(
                    ov["total_jobs_planned_employees"]
                )
            assert (
                deal.total_jobs_planned_daily_workers
                == ov["total_jobs_planned_daily_workers"]
            )
            assert deal.total_jobs_current == ov["total_jobs_current"]
            assert deal.total_jobs_created_comment == ov["total_jobs_created_comment"]
            assert deal.foreign_jobs_created == ov["foreign_jobs_created"]
            if deal.foreign_jobs_planned or ov["foreign_jobs_planned"]:
                print(deal.foreign_jobs_planned, ov["foreign_jobs_planned"])
                assert deal.foreign_jobs_planned == int(ov["foreign_jobs_planned"])
            if (
                deal.foreign_jobs_planned_employees
                or ov["foreign_jobs_planned_employees"]
            ):
                print(
                    deal.foreign_jobs_planned_employees,
                    ov["foreign_jobs_planned_employees"],
                )
                assert deal.foreign_jobs_planned_employees == int(
                    ov["foreign_jobs_planned_employees"]
                )
            assert (
                deal.foreign_jobs_planned_daily_workers
                == ov["foreign_jobs_planned_daily_workers"]
            )
            assert deal.foreign_jobs_current == ov["foreign_jobs_current"]
            assert (
                deal.foreign_jobs_created_comment == ov["foreign_jobs_created_comment"]
            )
            assert deal.domestic_jobs_created == ov["domestic_jobs_created"]

            if deal.domestic_jobs_planned or ov["domestic_jobs_planned"]:
                assert deal.domestic_jobs_planned == int(ov["domestic_jobs_planned"])
            assert (
                deal.domestic_jobs_planned_employees
                == ov["domestic_jobs_planned_employees"]
            )
            assert (
                deal.domestic_jobs_planned_daily_workers
                == ov["domestic_jobs_planned_daily_workers"]
            )
            assert deal.domestic_jobs_current == ov["domestic_jobs_current"]
            assert (
                deal.domestic_jobs_created_comment
                == ov["domestic_jobs_created_comment"]
            )
            print(deal.operating_company_id, ov["operating_company"])
            assert deal.operating_company_id == ov["operating_company"]
            # print(deal.involved_actors, ov["involved_actors"])
            # assert deal.involved_actors == ov["involved_actors"]
            assert deal.project_name == ov["project_name"]
            assert deal.investment_chain_comment == ov["investment_chain_comment"]
            # assert deal.datasources == ov["datasources"]
            assert deal.name_of_community == ov["name_of_community"]
            assert deal.name_of_indigenous_people == ov["name_of_indigenous_people"]
            assert deal.people_affected_comment == ov["people_affected_comment"]
            assert deal.recognition_status == ov["recognition_status"]
            assert deal.recognition_status_comment == ov["recognition_status_comment"]
            assert deal.community_consultation == ov["community_consultation"]
            assert (
                deal.community_consultation_comment
                == ov["community_consultation_comment"]
            )
            assert deal.community_reaction == ov["community_reaction"]
            assert deal.community_reaction_comment == ov["community_reaction_comment"]
            assert deal.land_conflicts == ov["land_conflicts"]
            assert deal.land_conflicts_comment == ov["land_conflicts_comment"]
            assert deal.displacement_of_people == ov["displacement_of_people"]
            if deal.displaced_people or ov["displaced_people"]:
                assert deal.displaced_people == int(ov["displaced_people"])
            if deal.displaced_households or ov["displaced_households"]:
                print(deal.displaced_households, int(ov["displaced_households"]))
                assert deal.displaced_households == int(ov["displaced_households"])
            if (
                deal.displaced_people_from_community_land
                or ov["displaced_people_from_community_land"]
            ):
                assert deal.displaced_people_from_community_land == int(
                    ov["displaced_people_from_community_land"]
                )
            assert (
                deal.displaced_people_within_community_land
                == ov["displaced_people_within_community_land"]
            )
            if (
                deal.displaced_households_from_fields
                or ov["displaced_households_from_fields"]
            ):
                print(
                    deal.displaced_households_from_fields,
                    ov["displaced_households_from_fields"],
                )
                assert deal.displaced_households_from_fields == int(
                    ov["displaced_households_from_fields"]
                )
            if (
                deal.displaced_people_on_completion
                or ov["displaced_people_on_completion"]
            ):
                assert deal.displaced_people_on_completion == int(
                    ov["displaced_people_on_completion"]
                )
            assert (
                deal.displacement_of_people_comment
                == ov["displacement_of_people_comment"]
            )
            assert deal.negative_impacts == ov["negative_impacts"]
            assert deal.negative_impacts_comment == ov["negative_impacts_comment"]
            assert deal.promised_compensation == ov["promised_compensation"]
            assert deal.received_compensation == ov["received_compensation"]
            assert deal.promised_benefits == ov["promised_benefits"]
            assert deal.promised_benefits_comment == ov["promised_benefits_comment"]
            assert deal.materialized_benefits == ov["materialized_benefits"]
            assert (
                deal.materialized_benefits_comment
                == ov["materialized_benefits_comment"]
            )
            assert deal.presence_of_organizations == ov["presence_of_organizations"]
            assert deal.former_land_owner == ov["former_land_owner"]
            assert deal.former_land_owner_comment == ov["former_land_owner_comment"]
            assert deal.former_land_use == ov["former_land_use"]
            assert deal.former_land_use_comment == ov["former_land_use_comment"]
            assert deal.former_land_cover == ov["former_land_cover"]
            assert deal.former_land_cover_comment == ov["former_land_cover_comment"]
            assert deal.crops == ov["crops"]
            assert deal.crops_comment == ov["crops_comment"]
            assert deal.animals == ov["animals"]
            assert deal.animals_comment == ov["animals_comment"]
            assert deal.mineral_resources == ov["mineral_resources"]
            assert deal.mineral_resources_comment == ov["mineral_resources_comment"]
            assert deal.contract_farming_crops == ov["contract_farming_crops"]
            assert (
                deal.contract_farming_crops_comment
                == ov["contract_farming_crops_comment"]
            )
            assert deal.contract_farming_animals == ov["contract_farming_animals"]
            assert (
                deal.contract_farming_animals_comment
                == ov["contract_farming_animals_comment"]
            )
            assert deal.has_domestic_use == ov["has_domestic_use"]
            if deal.domestic_use or ov["domestic_use"]:
                print(deal.domestic_use, ov["domestic_use"])
                assert deal.domestic_use == float(ov["domestic_use"])
            assert deal.has_export == ov["has_export"]
            if deal.export or ov["export"]:
                print(deal.export, ov["export"])
                assert deal.export == float(ov["export"])
            assert deal.export_country1_id == ov["export_country1"]
            assert deal.export_country1_ratio == ov["export_country1_ratio"]
            assert deal.export_country2_id == ov["export_country2"]
            assert deal.export_country2_ratio == ov["export_country2_ratio"]
            assert deal.export_country3_id == ov["export_country3"]
            assert deal.export_country3_ratio == ov["export_country3_ratio"]
            assert deal.use_of_produce_comment == ov["use_of_produce_comment"]
            assert deal.in_country_processing == ov["in_country_processing"]
            assert (
                deal.in_country_processing_comment
                == ov["in_country_processing_comment"]
            )
            assert (
                deal.in_country_processing_facilities
                == ov["in_country_processing_facilities"]
            )
            assert deal.in_country_end_products == ov["in_country_end_products"]
            print(deal.water_extraction_envisaged, ov["water_extraction_envisaged"])
            assert deal.water_extraction_envisaged == ov["water_extraction_envisaged"]
            assert (
                deal.water_extraction_envisaged_comment
                == ov["water_extraction_envisaged_comment"]
            )
            assert deal.source_of_water_extraction == ov["source_of_water_extraction"]
            assert (
                deal.source_of_water_extraction_comment
                == ov["source_of_water_extraction_comment"]
            )
            assert (
                deal.how_much_do_investors_pay_comment
                == ov["how_much_do_investors_pay_comment"]
            )
            assert deal.water_extraction_amount == ov["water_extraction_amount"]
            assert (
                deal.water_extraction_amount_comment
                == ov["water_extraction_amount_comment"]
            )
            assert (
                deal.use_of_irrigation_infrastructure
                == ov["use_of_irrigation_infrastructure"]
            )
            assert (
                deal.use_of_irrigation_infrastructure_comment
                == ov["use_of_irrigation_infrastructure_comment"]
            )
            assert deal.water_footprint == ov["water_footprint"]
            assert deal.gender_related_information == ov["gender_related_information"]
            assert deal.overall_comment == ov["overall_comment"]

            #### calculated
            assert deal.is_public == ov["is_public"]
            assert deal.has_known_investor == ov["has_known_investor"]
            # parent_companies = []
            # for pid in ov["parent_companies"]:
            #     try:
            #         parent_companies += [Investor.objects.get(id=pid)]
            #     except Investor.DoesNotExist:
            #         pass
            # # noinspection PyUnresolvedReferences
            # nv.parent_companies.set(parent_companies)
            # top_investors = []
            # for pid in ov["top_investors"]:
            #     try:
            #         top_investors += [Investor.objects.get(id=pid)]
            #     except Investor.DoesNotExist:
            #         pass
            # # noinspection PyUnresolvedReferences
            # nv.top_investors.set(top_investors)
            if deal.current_contract_size or ov["current_contract_size"]:
                print(deal.current_contract_size, ov["current_contract_size"])
                assert round(float(deal.current_contract_size), 2) == round(
                    ov["current_contract_size"], 2
                )
            if deal.current_production_size or ov["current_production_size"]:
                assert round(float(deal.current_production_size), 2) == round(
                    ov["current_production_size"], 2
                )
            assert (
                deal.current_intention_of_investment
                == ov["current_intention_of_investment"]
            )
            assert deal.current_negotiation_status == ov["current_negotiation_status"]
            assert (
                deal.current_implementation_status
                == ov["current_implementation_status"]
            )
            assert deal.current_crops == ov["current_crops"]
            assert deal.current_animals == ov["current_animals"]
            assert deal.current_mineral_resources == ov["current_mineral_resources"]
            if deal.deal_size or ov["deal_size"]:
                assert round(float(deal.deal_size), 2) == round(ov["deal_size"], 2)
            assert deal.initiation_year == ov["initiation_year"]
            assert deal.forest_concession == ov["forest_concession"]
            print(deal.transnational, ov["transnational"])
            assert deal.transnational == ov["transnational"]

            # assert deal.fully_updated == ov["fully_updated"]

            # assert deal.created_by_id == old_deal_version.created_by_id
            # assert deal.created_at == old_deal_version.created_at
