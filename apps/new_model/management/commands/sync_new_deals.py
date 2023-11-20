from django.core.management.base import BaseCommand
from icecream import ic

from apps.landmatrix.models.deal import Deal, DealWorkflowInfo, DealVersion
from apps.landmatrix.models.investor import Investor
from apps.new_model.models import (
    DealHull,
    DealVersion2,
    Location,
    Area,
    Contract,
    DealDataSource,
    InvestorHull,
)

from django.contrib.gis.geos import Point, GEOSGeometry


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO HANDLE THESE
        exclude_ids = [
            3523,
            3536,
            4862,
            4863,
            4864,
            4865,
            4866,
            4867,
            4868,
            4869,
            4882,
            4883,
            5400,  # datasources[4] has `type=None` instead of `type=''`
            5410,  # datasources[2] has `type=None` instead of `type=''`
            5415,  # datasources[2] has `type=None` instead of `type=''`
            5416,  # datasources[3] has `type=None` instead of `type=''`
            5871,  # weird
            6174,  # "LAFP"?
            6177,  # "LAFP"?
            6178,  # "LAFP"?
            6179,  # "LAFP"?
            6181,  # "LAFP"?
            6182,  # "LAFP"?
            6183,  # "LAFP"?
            6184,  # "LAFP"?
            6192,  # broken investor link
            # TODO
            6237,  # broken investor link
            6243,  # broken investor link
            9422,  # broken investor link
            9646,  # broken investor link
        ]
        deals = (
            Deal.objects.all()
            .order_by("id")
            .exclude(id__in=exclude_ids)
            # .prefetch_related("versions")
            # .all()[:1000]
            .filter(id__in=[3, 23, 4747])
            # .filter(id=2)
        )
        for old_deal in deals:  # type: Deal
            ## WIP:
            # version_dings = [
            #     [x.serialized_data["status"], x.serialized_data["draft_status"]]
            #     for x in old_deal.versions.all().order_by("id")
            # ]
            # match version_dings:
            #     case [[1, other_v]]:
            #         print(old_deal.id, "ohoa", other_v)
            #     case _:
            #         continue

            # if version_dings == [[2, None], [3, None], [3, 4], [4, None]]:
            #     pass
            # else:
            #     print("UNKNOWN", version_dings)
            #     return

            deal_hull: DealHull
            deal_hull, _ = DealHull.objects.get_or_create(
                id=old_deal.id,
                created_by=old_deal.created_by,
                created_at=old_deal.created_at,
            )

            deal_hull.fully_updated_at = old_deal.fully_updated_at

            print(old_deal.id, "status:", old_deal.status)
            for old_version in old_deal.versions.all().order_by("id"):
                new_version: DealVersion2
                base_payload = {
                    "deal_id": old_deal.id,
                    "id": old_version.id,
                    "created_at": old_version.created_at,
                    "created_by_id": old_version.created_by_id,
                    "modified_at": old_version.modified_at,
                    "modified_by_id": old_version.modified_by_id,
                }
                try:
                    new_version = DealVersion2.objects.get(**base_payload)
                except DealVersion2.DoesNotExist:
                    new_version = DealVersion2(**base_payload)

                old_version_dict = old_version.serialized_data

                map_version_payload(old_version_dict, new_version)

                deal_hull.country_id = old_version_dict["country"]

                if old_version_dict["status"] == 1:
                    map_dings = {
                        1: "DRAFT",
                        2: "REVIEW",
                        3: "ACTIVATION",
                        4: "REJECTED",
                        5: "TO_DELETE",
                    }
                    new_version.status = map_dings[old_version_dict["draft_status"]]
                    deal_hull.draft_version_id = old_version.id
                elif old_version_dict["status"] in [2, 3]:
                    if old_version_dict["draft_status"] is None:
                        new_version.status = "ACTIVATED"
                        deal_hull.active_version_id = old_version.id
                        deal_hull.draft_version_id = None
                    elif old_version_dict["draft_status"] == 1:
                        new_version.status = "DRAFT"
                        deal_hull.draft_version_id = old_version.id
                    elif old_version_dict["draft_status"] == 2:
                        new_version.status = "REVIEW"
                        deal_hull.draft_version_id = old_version.id
                    elif old_version_dict["draft_status"] == 3:
                        new_version.status = "ACTIVATION"
                        deal_hull.draft_version_id = old_version.id
                    elif old_version_dict["draft_status"] == 4:
                        new_version.status = "REJECTED"
                        # deal_hull.active_version_id = deal_version.id
                    else:
                        # print("TODO?!", old_version_dict["draft_status"])
                        new_version.status = "DELETED"
                elif old_version_dict["status"] == 4:
                    if old_version_dict["draft_status"] is None:
                        new_version.status = "TO_DELETE"
                        deal_hull.active_version_id = old_version.id
                    else:
                        print("TODO DELETE else?!")
                        ...  # TODO !!
                else:
                    print("VERSION OHO", old_deal.id, old_version_dict["status"])
                    # return
                # print(old_version.workflowinfos.all())
                new_version.save(
                    recalculate_dependent=False, recalculate_independent=False
                )

            # deal_hull.draft_version_id = old_deal.current_draft_id
            deal_hull.deleted = old_deal.status == 4
            deal_hull.confidential = old_deal.confidential
            deal_hull.confidential_comment = old_deal.confidential_comment

            do_workflows(old_deal.id)

            deal_hull.save()


def map_locations(nv: DealVersion2, locations: list[dict]):
    for loc in locations:
        l1, _ = Location.objects.get_or_create(dealversion_id=nv.id, nid=loc["id"])
        l1.name = loc["name"]
        l1.description = loc["description"]
        if p := loc["point"]:
            l1.point = Point(p["lng"], p["lat"])
        l1.facility_name = loc["facility_name"]
        l1.level_of_accuracy = loc["level_of_accuracy"]
        l1.comment = loc["comment"]
        l1.save()
        if area := loc["areas"]:
            for feat in area["features"]:
                a1, _ = Area.objects.update_or_create(
                    location=l1,
                    area=GEOSGeometry(str(feat["geometry"])),
                    defaults={
                        "type": feat["properties"]["type"],
                        "current": feat["properties"].get("current", False),
                        "date": feat["properties"].get("date"),
                    },
                )


def map_contracts(nv: DealVersion2, contracts: list[dict]):
    for con in contracts:
        c1, _ = Contract.objects.get_or_create(dealversion_id=nv.id, nid=con["id"])
        c1.number = con["number"]
        c1.date = con.get("date", None)
        c1.expiration_date = con.get("expiration_date", None)
        c1.agreement_duration = con.get("agreement_duration", None)
        c1.comment = con.get("comment", "")
        c1.save()


def map_datasources(nv: DealVersion2, datasources: list[dict]):
    for dats in datasources:
        ds1, _ = DealDataSource.objects.get_or_create(
            dealversion_id=nv.id, nid=dats["id"]
        )
        ds1.type = dats.get("type", "")
        ds1.url = dats.get("url", "")
        if dats.get("file"):
            ds1.file.name = dats["file"]
        ds1.file_not_public = dats.get("file_not_public", False)
        ds1.publication_title = dats.get("publication_title", "")
        ds1.date = dats.get("date")
        ds1.name = dats.get("name", "")
        ds1.company = dats.get("company", "")
        ds1.email = dats.get("email", "")
        ds1.phone = dats.get("phone", "")
        ds1.includes_in_country_verified_information = dats.get(
            "includes_in_country_verified_information", ""
        )
        ds1.open_land_contracts_id = dats.get("open_land_contracts_id", "")
        ds1.comment = dats.get("comment", "")
        ds1.save()


def map_version_payload(ov: dict, nv: DealVersion2):
    # nv.country_id = ov["country"]
    nv.intended_size = ov["intended_size"]
    nv.contract_size = ov["contract_size"] or []
    nv.production_size = ov["production_size"] or []
    nv.land_area_comment = ov["land_area_comment"]
    nv.intention_of_investment = ov["intention_of_investment"]
    nv.intention_of_investment_comment = ov["intention_of_investment_comment"]
    nv.nature_of_deal = ov["nature_of_deal"] or []
    nv.nature_of_deal_comment = ov["nature_of_deal_comment"]
    nv.negotiation_status = ov["negotiation_status"] or []
    nv.negotiation_status_comment = ov["negotiation_status_comment"]
    nv.implementation_status = ov["implementation_status"] or []
    nv.implementation_status_comment = ov["implementation_status_comment"]
    nv.purchase_price = ov["purchase_price"]
    nv.purchase_price_currency_id = ov["purchase_price_currency"]
    nv.purchase_price_type = ov["purchase_price_type"]
    nv.purchase_price_area = ov["purchase_price_area"]
    nv.purchase_price_comment = ov["purchase_price_comment"]
    nv.annual_leasing_fee = ov["annual_leasing_fee"]
    nv.annual_leasing_fee_currency_id = ov["annual_leasing_fee_currency"]
    nv.annual_leasing_fee_type = ov["annual_leasing_fee_type"]
    nv.annual_leasing_fee_area = ov["annual_leasing_fee_area"]
    nv.annual_leasing_fee_comment = ov["annual_leasing_fee_comment"]
    nv.contract_farming = ov["contract_farming"]
    nv.on_the_lease_state = ov["on_the_lease_state"]
    nv.on_the_lease = ov["on_the_lease"] or []
    nv.off_the_lease_state = ov["off_the_lease_state"]
    nv.off_the_lease = ov["off_the_lease"] or []
    nv.contract_farming_comment = ov["contract_farming_comment"]
    nv.total_jobs_created = ov["total_jobs_created"]
    nv.total_jobs_planned = ov["total_jobs_planned"]
    nv.total_jobs_planned_employees = ov["total_jobs_planned_employees"]
    nv.total_jobs_planned_daily_workers = ov["total_jobs_planned_daily_workers"]
    nv.total_jobs_current = ov["total_jobs_current"] or []
    nv.total_jobs_created_comment = ov["total_jobs_created_comment"]
    nv.foreign_jobs_created = ov["foreign_jobs_created"]
    nv.foreign_jobs_planned = ov["foreign_jobs_planned"]
    nv.foreign_jobs_planned_employees = ov["foreign_jobs_planned_employees"]
    nv.foreign_jobs_planned_daily_workers = ov["foreign_jobs_planned_daily_workers"]
    nv.foreign_jobs_current = ov["foreign_jobs_current"] or []
    nv.foreign_jobs_created_comment = ov["foreign_jobs_created_comment"]
    nv.domestic_jobs_created = ov["domestic_jobs_created"]
    nv.domestic_jobs_planned = ov["domestic_jobs_planned"]
    nv.domestic_jobs_planned_employees = ov["domestic_jobs_planned_employees"]
    nv.domestic_jobs_planned_daily_workers = ov["domestic_jobs_planned_daily_workers"]
    nv.domestic_jobs_current = ov["domestic_jobs_current"] or []
    nv.domestic_jobs_created_comment = ov["domestic_jobs_created_comment"]
    if oid := ov["operating_company"]:
        all_versions = InvestorHull.objects.get(id=oid).versions.all()
        versions = all_versions.order_by("-created_at").filter(
            created_at__lte=ov["modified_at"]
        )
        if versions:
            nv.operating_company_id = versions.first().id
        else:
            nv.operating_company_id = all_versions.last().id

    nv.involved_actors = ov["involved_actors"] or []
    nv.project_name = ov["project_name"]
    nv.investment_chain_comment = ov["investment_chain_comment"]
    nv.name_of_community = ov["name_of_community"] or []
    nv.name_of_indigenous_people = ov["name_of_indigenous_people"] or []
    nv.people_affected_comment = ov["people_affected_comment"]
    nv.recognition_status = ov["recognition_status"] or []
    nv.recognition_status_comment = ov["recognition_status_comment"]
    nv.community_consultation = ov["community_consultation"]
    nv.community_consultation_comment = ov["community_consultation_comment"]
    nv.community_reaction = ov["community_reaction"]
    nv.community_reaction_comment = ov["community_reaction_comment"]
    nv.land_conflicts = ov["land_conflicts"]
    nv.land_conflicts_comment = ov["land_conflicts_comment"]
    nv.displacement_of_people = ov["displacement_of_people"]
    nv.displaced_people = ov["displaced_people"]
    nv.displaced_households = ov["displaced_households"]
    nv.displaced_people_from_community_land = ov["displaced_people_from_community_land"]
    nv.displaced_people_within_community_land = ov[
        "displaced_people_within_community_land"
    ]
    nv.displaced_households_from_fields = ov["displaced_households_from_fields"]
    nv.displaced_people_on_completion = ov["displaced_people_on_completion"]
    nv.displacement_of_people_comment = ov["displacement_of_people_comment"]
    nv.negative_impacts = ov["negative_impacts"] or []
    nv.negative_impacts_comment = ov["negative_impacts_comment"]
    nv.promised_compensation = ov["promised_compensation"]
    nv.received_compensation = ov["received_compensation"]
    nv.promised_benefits = ov["promised_benefits"] or []
    nv.promised_benefits_comment = ov["promised_benefits_comment"]
    nv.materialized_benefits = ov["materialized_benefits"] or []
    nv.materialized_benefits_comment = ov["materialized_benefits_comment"]
    nv.presence_of_organizations = ov["presence_of_organizations"]
    nv.former_land_owner = ov["former_land_owner"] or []
    nv.former_land_owner_comment = ov["former_land_owner_comment"]
    nv.former_land_use = ov["former_land_use"] or []
    nv.former_land_use_comment = ov["former_land_use_comment"]
    nv.former_land_cover = ov["former_land_cover"] or []
    nv.former_land_cover_comment = ov["former_land_cover_comment"]
    nv.crops = ov["crops"] or []
    nv.crops_comment = ov["crops_comment"]
    nv.animals = ov["animals"] or []
    nv.animals_comment = ov["animals_comment"]
    nv.mineral_resources = ov["mineral_resources"] or []
    nv.mineral_resources_comment = ov["mineral_resources_comment"]
    nv.contract_farming_crops = ov["contract_farming_crops"] or []
    nv.contract_farming_crops_comment = ov["contract_farming_crops_comment"]
    nv.contract_farming_animals = ov["contract_farming_animals"] or []
    nv.contract_farming_animals_comment = ov["contract_farming_animals_comment"]
    nv.electricity_generation = ov.get("electricity_generation") or []
    nv.electricity_generation_comment = ov.get("electricity_generation_comment") or ""
    nv.carbon_sequestration = ov.get("carbon_sequestration") or []
    nv.carbon_sequestration_comment = ov.get("carbon_sequestration_comment") or ""
    nv.has_domestic_use = ov["has_domestic_use"]
    nv.domestic_use = ov["domestic_use"]
    nv.has_export = ov["has_export"]
    nv.export = ov["export"]
    nv.export_country1_id = ov["export_country1"]
    nv.export_country1_ratio = ov["export_country1_ratio"]
    nv.export_country2_id = ov["export_country2"]
    nv.export_country2_ratio = ov["export_country2_ratio"]
    nv.export_country3_id = ov["export_country3"]
    nv.export_country3_ratio = ov["export_country3_ratio"]
    nv.use_of_produce_comment = ov["use_of_produce_comment"]
    nv.in_country_processing = ov["in_country_processing"]
    nv.in_country_processing_comment = ov["in_country_processing_comment"]
    nv.in_country_processing_facilities = ov["in_country_processing_facilities"]
    nv.in_country_end_products = ov["in_country_end_products"]
    nv.water_extraction_envisaged = ov["water_extraction_envisaged"]
    nv.water_extraction_envisaged_comment = ov["water_extraction_envisaged_comment"]
    nv.source_of_water_extraction = ov["source_of_water_extraction"] or []
    nv.source_of_water_extraction_comment = ov["source_of_water_extraction_comment"]
    nv.how_much_do_investors_pay_comment = ov["how_much_do_investors_pay_comment"]
    nv.water_extraction_amount = ov["water_extraction_amount"]
    nv.water_extraction_amount_comment = ov["water_extraction_amount_comment"]
    nv.use_of_irrigation_infrastructure = ov["use_of_irrigation_infrastructure"]
    nv.use_of_irrigation_infrastructure_comment = ov[
        "use_of_irrigation_infrastructure_comment"
    ]
    nv.water_footprint = ov["water_footprint"]
    nv.gender_related_information = ov["gender_related_information"]
    nv.overall_comment = ov["overall_comment"]

    nv.save(recalculate_dependent=False, recalculate_independent=False)

    map_locations(nv, ov["locations"])
    map_contracts(nv, ov["contracts"])
    map_datasources(nv, ov["datasources"])

    # ### calculated
    nv.is_public = ov["is_public"]
    nv.has_known_investor = ov["has_known_investor"]
    parent_companies = []
    for pid in ov["parent_companies"]:
        try:
            parent_companies += [Investor.objects.get(id=pid)]
        except Investor.DoesNotExist:
            pass
    # noinspection PyUnresolvedReferences
    nv.parent_companies.set(parent_companies)
    top_investors = []
    for pid in ov["top_investors"]:
        try:
            top_investors += [Investor.objects.get(id=pid)]
        except Investor.DoesNotExist:
            pass
    # noinspection PyUnresolvedReferences
    nv.top_investors.set(top_investors)
    nv.current_contract_size = ov["current_contract_size"]
    nv.current_production_size = ov["current_production_size"]
    nv.current_intention_of_investment = ov["current_intention_of_investment"] or []

    nv.current_negotiation_status = ov["current_negotiation_status"] or []
    nv.current_implementation_status = ov["current_implementation_status"] or []
    nv.current_crops = ov["current_crops"] or []
    nv.current_animals = ov["current_animals"] or []
    nv.current_mineral_resources = ov["current_mineral_resources"] or []
    nv.current_electricity_generation = ov.get("current_electricity_generation") or []
    nv.current_carbon_sequestration = ov.get("current_carbon_sequestration") or []
    nv.deal_size = ov["deal_size"]
    nv.initiation_year = ov["initiation_year"]
    nv.forest_concession = ov["forest_concession"]
    nv.transnational = ov["transnational"]

    nv.fully_updated = ov["fully_updated"]


def do_workflows(deal_id):
    for dwi in DealWorkflowInfo.objects.filter(deal_id=deal_id):
        if not dwi.deal_version_id:
            continue
        # if dwi.deal_version_id in [43461, 43462]:
        #     print(dwi, dwi.draft_status_before, dwi.draft_status_after, dwi.comment)
        dv: DealVersion2 = DealVersion2.objects.get(id=dwi.deal_version_id)
        if dwi.draft_status_before is None and dwi.draft_status_after == 1:
            ...  # TODO new draft.. what to do?
        elif dwi.draft_status_before in [2, 3] and dwi.draft_status_after == 1:
            ...  # TODO new draft.. what to do?
        elif (dwi.draft_status_before is None and dwi.draft_status_after is None) or (
            dwi.draft_status_before == dwi.draft_status_after
        ):
            ...  # nothing?
        elif dwi.draft_status_before in [None, 1] and dwi.draft_status_after == 2:
            dv.sent_to_review_at = dwi.timestamp
            dv.sent_to_review_by = dwi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
        elif dwi.draft_status_before == 2 and dwi.draft_status_after == 3:
            dv.reviewed_at = dwi.timestamp
            dv.reviewed_by = dwi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
            # dv.status
        elif dwi.draft_status_before in [2, 3] and dwi.draft_status_after is None:
            dv.activated_at = dwi.timestamp
            dv.activated_by = dwi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
        elif dwi.draft_status_before == 4 or dwi.draft_status_after == 4:
            ...  # deleted status change
        else:
            ...
            print(
                "DWI OHO",
                dwi.deal_id,
                dwi.draft_status_before,
                dwi.draft_status_after,
                dwi.comment,
            )
