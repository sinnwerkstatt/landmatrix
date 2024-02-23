import sys

from django.contrib.gis.geos import Point, GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import connection
from icecream import ic

from apps.landmatrix.models.deal import DealOld, DealWorkflowInfoOld
from apps.landmatrix.models.new import (
    DealHull,
    DealVersion,
    Location,
    Area,
    Contract,
    DealDataSource,
    InvestorHull,
    DealWorkflowInfo,
)

status_map_dings = {
    1: "DRAFT",
    2: "REVIEW",
    3: "ACTIVATION",
    4: "REVIEW",
    5: "DRAFT",
    None: None,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("start_id", nargs="?", type=int)
        parser.add_argument("end_id", nargs="?", type=int)

    def handle(self, *args, **options):
        exclude_ids = []
        deals = DealOld.objects.all().order_by("id").exclude(id__in=exclude_ids)
        if options["start_id"]:
            deals = deals.filter(id__gte=options["start_id"])
        if options["end_id"]:
            deals = deals.filter(id__lte=options["end_id"])
        for old_deal in deals:  # type: DealOld
            url = f"https://landmatrix.org/deal/{old_deal.id}/"
            ic(old_deal.id, old_deal.status, url)

            deal_hull: DealHull
            deal_hull, _ = DealHull.objects.get_or_create(
                id=old_deal.id,
                first_created_by_id=old_deal.created_by_id or 1,
                first_created_at=old_deal.created_at,
            )

            deal_hull.fully_updated_at = old_deal.fully_updated_at

            for old_version in old_deal.versions.all().order_by("id"):
                # ic(old_version.id)
                new_version: DealVersion
                base_payload = {
                    "deal_id": old_deal.id,
                    "id": old_version.id,
                    "created_at": old_version.created_at,
                    "created_by_id": old_version.created_by_id,
                    "modified_at": old_version.modified_at,
                    "modified_by_id": old_version.modified_by_id,
                }
                try:
                    new_version = DealVersion.objects.get(**base_payload)
                except DealVersion.DoesNotExist:
                    new_version = DealVersion(**base_payload)

                old_version_dict = old_version.serialized_data

                map_version_payload(old_version_dict, new_version)

                deal_hull.country_id = old_version_dict["country"]

                if old_version_dict["status"] == 1:
                    new_version.status = status_map_dings[
                        old_version_dict["draft_status"]
                    ]
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
                        new_version.status = "REVIEW"
                        # deal_hull.active_version_id = deal_version.id
                    else:
                        # TODO shall we finally just delete these?
                        new_version.status = "DELETED"
                elif old_version_dict["status"] == 4:
                    if old_version_dict["draft_status"] is None:
                        new_version.status = "DRAFT"
                        deal_hull.active_version_id = old_version.id
                    else:
                        print("TODO DELETE else?!")
                        ...  # TODO !!
                else:
                    print("VERSION OHO", old_deal.id, old_version_dict["status"])
                    # return

                new_version.save(
                    recalculate_dependent=False, recalculate_independent=False
                )

            deal_hull.deleted = old_deal.status == 4
            deal_hull.confidential = old_deal.confidential
            deal_hull.confidential_comment = old_deal.confidential_comment or ""

            do_workflows(old_deal.id)

            deal_hull.save()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval('landmatrix_dealhull_id_seq', (SELECT MAX(id) from landmatrix_dealhull))"
            )
            cursor.execute(
                "SELECT setval('landmatrix_dealversion_id_seq', (SELECT MAX(id) from landmatrix_dealversion))"
            )
            cursor.execute(
                "SELECT setval('landmatrix_dealworkflowinfo_id_seq', (SELECT MAX(id) from landmatrix_dealworkflowinfo))"
            )


def map_locations(nv: DealVersion, locations: list[dict]):
    for loc in locations:
        l1, _ = Location.objects.get_or_create(dealversion_id=nv.id, nid=loc["id"])
        l1.name = loc.get("name", "")
        l1.description = loc.get("description", "")
        if p := loc.get("point"):
            l1.point = Point(p["lng"], p["lat"])
        l1.facility_name = loc.get("facility_name", "")
        l1.level_of_accuracy = loc.get("level_of_accuracy", "")
        l1.comment = loc.get("comment", "")
        l1.save()
        if area := loc.get("areas"):
            Area.objects.filter(location=l1).delete()
            for feat in area["features"]:
                Area.objects.create(
                    location=l1,
                    area=Area.geometry_to_multipolygon(feat["geometry"]),
                    type=feat["properties"]["type"],
                    current=feat["properties"].get("current", False),
                    date=feat["properties"].get("date"),
                )


def map_contracts(nv: DealVersion, contracts: list[dict]):
    for con in contracts:
        c1, _ = Contract.objects.get_or_create(dealversion_id=nv.id, nid=con["id"])
        c1.number = con.get("number", "")
        c1.date = con.get("date", None)
        c1.expiration_date = con.get("expiration_date", None)
        c1.agreement_duration = con.get("agreement_duration", None)
        c1.comment = con.get("comment", "")
        c1.save()


def map_datasources(nv: DealVersion, datasources: list[dict]):
    for dats in datasources:
        ds1, _ = DealDataSource.objects.get_or_create(
            dealversion_id=nv.id, nid=dats["id"]
        )
        if ds_type := dats.get("type"):
            ds1.type = ds_type
        else:
            ds1.type = "OTHER"
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


def map_version_payload(ov: dict, nv: DealVersion):
    nv.intended_size = ov["intended_size"]
    nv.contract_size = []
    for x in ov["contract_size"] or []:
        if x.get("area") is None:
            continue
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        else:
            x["date"] = x["date"].strip()
            match x["date"]:
                case "6":
                    x["date"] = None
                case "11996":
                    x["date"] = "1996"
                case "2020-04-00":
                    x["date"] = "2020-04"
                case "12017":
                    x["date"] = "2017"
                case "11993":
                    x["date"] = "1993"
                case "3":
                    x["date"] = "2030"
                case "2007-31-03":
                    x["date"] = "2007-03-31"
                case "201133912":
                    x["date"] = "2011-01-12"

        if nv.deal_id == 5177 and x.get("date") == "7":
            x["date"] = "2016"
        if nv.deal_id == 5483 and x.get("date") == "1":
            x["date"] = None

        nv.contract_size += [x]

    nv.production_size = []
    for x in ov["production_size"] or []:
        if x.get("area") is None:
            continue
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        else:
            x["date"] = x["date"].strip()
            match x["date"]:
                case "20111":
                    x["date"] = "2011"
                case "2007-31-03":
                    x["date"] = "2007-03-31"
                case "6":
                    x["date"] = None

        if nv.deal_id == 5483 and x.get("date") == "12":
            x["date"] = None

        nv.production_size += [x]

    nv.land_area_comment = ov["land_area_comment"]
    nv.intention_of_investment = []
    for x in ov["intention_of_investment"] or []:
        if not x.get("choices"):
            continue
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        else:
            x["date"] = x["date"].strip()
        if not x.get("area"):
            x["area"] = None
        nv.intention_of_investment += [x]

    nv.intention_of_investment_comment = ov["intention_of_investment_comment"]
    nv.nature_of_deal = ov["nature_of_deal"] or []
    nv.nature_of_deal_comment = ov["nature_of_deal_comment"]
    nv.negotiation_status = []
    for neg in ov["negotiation_status"] or []:
        if not neg.get("choice"):
            continue
        if not neg.get("current"):
            neg["current"] = False
        if not neg.get("date"):
            neg["date"] = None
        else:
            neg["date"] = neg["date"].strip()

        if nv.deal_id == 4009 and neg.get("date") == "201":
            neg["date"] = "2012"
        elif nv.deal_id == 5173 and neg.get("date") == "1":
            neg["date"] = "2016"
        nv.negotiation_status += [neg]

    nv.negotiation_status_comment = ov["negotiation_status_comment"]

    nv.implementation_status = []
    for x in ov["implementation_status"] or []:
        if not x.get("choice"):
            continue
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        if x.get("date") == "6":
            x["date"] = None
        if nv.deal_id == 6012 and x.get("date") == "30":
            x["date"] = None

        nv.implementation_status += [x]

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
    for x in nv.on_the_lease:
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        for p in ["area", "farmers", "households"]:
            if not x.get(p):
                x[p] = None
        if x.get("farmers"):
            x["farmers"] = int(x["farmers"])

    nv.off_the_lease_state = ov["off_the_lease_state"]
    nv.off_the_lease = ov["off_the_lease"] or []
    for x in nv.off_the_lease:
        if not x.get("current"):
            x["current"] = False
        if not x.get("date"):
            x["date"] = None
        if not x.get("area"):
            x["area"] = None
        if "farmers" in x.keys():
            x["farmers"] = int(x["farmers"])
        else:
            x["farmers"] = None
        if not x.get("households"):
            x["households"] = None

    nv.contract_farming_comment = ov["contract_farming_comment"]
    nv.total_jobs_created = ov["total_jobs_created"]
    nv.total_jobs_planned = ov["total_jobs_planned"]
    nv.total_jobs_planned_employees = ov["total_jobs_planned_employees"]
    nv.total_jobs_planned_daily_workers = ov["total_jobs_planned_daily_workers"]
    nv.total_jobs_current = ov["total_jobs_current"] or []
    for jbs in nv.total_jobs_current:
        if not jbs.get("current"):
            jbs["current"] = False
        if not jbs.get("date"):
            jbs["date"] = None
        else:
            jbs["date"] = jbs["date"].strip()
        if not jbs.get("jobs"):
            jbs["jobs"] = None
        else:
            jbs["jobs"] = int(float(jbs["jobs"]))
        if jbs.get("workers") in ["", None]:
            jbs["workers"] = None
        else:
            jbs["workers"] = int(float(jbs["workers"]))

        if "employees" in jbs.keys() and jbs["employees"] is not None:
            jbs["employees"] = int(float(jbs["employees"]))
        else:
            jbs["employees"] = None
    nv.total_jobs_created_comment = ov["total_jobs_created_comment"]
    nv.foreign_jobs_created = ov["foreign_jobs_created"]
    nv.foreign_jobs_planned = ov["foreign_jobs_planned"]
    nv.foreign_jobs_planned_employees = ov["foreign_jobs_planned_employees"]
    nv.foreign_jobs_planned_daily_workers = ov["foreign_jobs_planned_daily_workers"]
    nv.foreign_jobs_current = ov["foreign_jobs_current"] or []
    for jbs in nv.foreign_jobs_current:
        if not jbs.get("current"):
            jbs["current"] = False
        if not jbs.get("date"):
            jbs["date"] = None
        else:
            jbs["date"] = jbs["date"].strip()
        if "jobs" in jbs.keys() and jbs["jobs"] is not None:
            jbs["jobs"] = int(float(jbs["jobs"]))
        else:
            jbs["jobs"] = None
        if "workers" in jbs.keys() and jbs["workers"] is not None:
            jbs["workers"] = int(float(jbs["workers"]))
        else:
            jbs["workers"] = None
        if "employees" in jbs.keys() and jbs["employees"] is not None:
            jbs["employees"] = int(float(jbs["employees"]))
        else:
            jbs["employees"] = None

    nv.foreign_jobs_created_comment = ov["foreign_jobs_created_comment"]
    nv.domestic_jobs_created = ov["domestic_jobs_created"]
    nv.domestic_jobs_planned = ov["domestic_jobs_planned"]
    nv.domestic_jobs_planned_employees = ov["domestic_jobs_planned_employees"]
    nv.domestic_jobs_planned_daily_workers = ov["domestic_jobs_planned_daily_workers"]
    nv.domestic_jobs_current = ov["domestic_jobs_current"] or []
    for jbs in nv.domestic_jobs_current:
        if not jbs.get("current"):
            jbs["current"] = False
        if not jbs.get("date"):
            jbs["date"] = None
        else:
            jbs["date"] = jbs["date"].strip()
        if "jobs" in jbs.keys() and jbs["jobs"] is not None:
            jbs["jobs"] = int(float(jbs["jobs"]))
        else:
            jbs["jobs"] = None
        if "workers" in jbs.keys() and jbs["workers"] is not None:
            jbs["workers"] = int(float(jbs["workers"]))
        else:
            jbs["workers"] = None
        if "employees" in jbs.keys() and jbs["employees"] is not None:
            jbs["employees"] = int(float(jbs["employees"]))
        else:
            jbs["employees"] = None

    nv.domestic_jobs_created_comment = ov["domestic_jobs_created_comment"]
    if oid := ov["operating_company"]:
        try:
            nv.operating_company_id = InvestorHull.objects.get(id=oid).id
        except InvestorHull.DoesNotExist:
            pass

    nv.involved_actors = ov["involved_actors"] or []
    for act in nv.involved_actors:
        if "name" in act.keys():
            act["name"] = (act.get("name") or "").strip()
        if "role" not in act.keys():
            act["role"] = "OTHER"

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
    nv.crops = []
    for crop in ov["crops"] or []:
        if not crop.get("choices"):
            continue
        if not crop.get("current"):
            crop["current"] = False
        if not crop.get("date"):
            crop["date"] = None
        else:
            crop["date"] = crop["date"].strip()

        crop["choices"] = [x for x in crop["choices"] if x not in ["35", "67"]]

        for p in ["area", "yield", "export"]:
            if not crop.get(p):
                crop[p] = None
        nv.crops += [crop]

    nv.crops_comment = ov["crops_comment"]

    nv.animals = []
    for animal in ov["animals"] or []:
        if not animal.get("choices"):
            continue
        if not animal.get("current"):
            animal["current"] = False
        if not animal.get("date"):
            animal["date"] = None

        animal["choices"] = [x for x in animal["choices"] if x != "1"]
        for p in ["area", "yield", "export"]:
            if not animal.get(p):
                animal[p] = None
        nv.animals += [animal]

    nv.animals_comment = ov["animals_comment"]

    nv.mineral_resources = []
    for mr in ov["mineral_resources"] or []:
        if not mr.get("choices"):
            continue
        if not mr.get("current"):
            mr["current"] = False
        if not mr.get("date"):
            mr["date"] = None
        add_properties = ["date", "area", "yield", "export"]
        for p in add_properties:
            if not mr.get(p):
                mr[p] = None
        mr["choices"] = [x for x in mr["choices"] if x not in ["PYN", "33"]]
        nv.mineral_resources += [mr]

    nv.mineral_resources_comment = ov["mineral_resources_comment"]

    nv.contract_farming_crops = []
    for cfc in ov["contract_farming_crops"] or []:
        if not cfc.get("choices"):
            continue
        if not cfc.get("current"):
            cfc["current"] = False
        if not cfc.get("area"):
            cfc["area"] = None
        if cfc.get("date"):
            cfc["date"] = cfc["date"].strip()
        else:
            cfc["date"] = None
        nv.contract_farming_crops += [cfc]

    nv.contract_farming_crops_comment = ov["contract_farming_crops_comment"]
    nv.contract_farming_animals = []
    for cfa in ov["contract_farming_animals"] or []:
        if not cfa.get("choices"):
            continue
        if not cfa.get("current"):
            cfa["current"] = False
        if not cfa.get("date"):
            cfa["date"] = None
        if not cfa.get("area"):
            cfa["area"] = None
        nv.contract_farming_animals += [cfa]

    nv.contract_farming_animals_comment = ov["contract_farming_animals_comment"]
    nv.electricity_generation = []
    for cfa in ov.get("electricity_generation") or []:
        if not cfa.get("current"):
            cfa["current"] = False

        for p in [
            "date",
            "area",
            "export",
            "windfarm_count",
            "current_capacity",
            "intended_capacity",
        ]:
            if not cfa.get(p):
                cfa[p] = None
        nv.electricity_generation += [cfa]
    nv.electricity_generation_comment = ov.get("electricity_generation_comment") or ""
    nv.carbon_sequestration = []
    for cfa in ov.get("carbon_sequestration") or []:
        if not cfa.get("current"):
            cfa["current"] = False

        if not cfa.get("certification_standard_name"):
            cfa["certification_standard_name"] = None
        if not cfa.get("certification_standard_comment"):
            cfa["certification_standard_comment"] = ""

        for p in [
            "date",
            "area",
            "projected_lifetime_sequestration",
            "projected_annual_sequestration",
            "certification_standard",
        ]:
            if cfa.get(p) is None:
                cfa[p] = None
        nv.carbon_sequestration += [cfa]

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

    # ic(ov)
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
            parent_companies += [InvestorHull.objects.get(id=pid)]
        except InvestorHull.DoesNotExist:
            pass
    # noinspection PyUnresolvedReferences
    nv.parent_companies.set(parent_companies)
    top_investors = []
    for pid in ov["top_investors"]:
        try:
            top_investors += [InvestorHull.objects.get(id=pid)]
        except InvestorHull.DoesNotExist:
            pass
    # noinspection PyUnresolvedReferences
    nv.top_investors.set(top_investors)
    nv.current_contract_size = ov["current_contract_size"]
    nv.current_production_size = ov["current_production_size"]
    nv.current_intention_of_investment = ov["current_intention_of_investment"] or []

    nv.current_negotiation_status = ov["current_negotiation_status"]
    nv.current_implementation_status = ov["current_implementation_status"]
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
    for wfi_old in DealWorkflowInfoOld.objects.filter(deal_id=deal_id):
        wfi_old: DealWorkflowInfoOld

        status_before = status_map_dings[wfi_old.draft_status_before]
        status_after = status_map_dings[wfi_old.draft_status_after]
        if status_before in ["REVIEW", "ACTIVATION"] and status_after is None:
            status_after = "ACTIVATED"

        wfi, _ = DealWorkflowInfo.objects.get_or_create(
            id=wfi_old.id,
            defaults={
                "from_user_id": wfi_old.from_user_id,
                "to_user_id": wfi_old.to_user_id,
                "status_before": status_before,
                "status_after": status_after,
                "timestamp": wfi_old.timestamp,
                "comment": wfi_old.comment or "",
                "replies": wfi_old.replies or [],
                "resolved": wfi_old.resolved,
                "deal_id": wfi_old.deal_id,
                "deal_version_id": wfi_old.deal_version_id,
            },
        )

        if not wfi.deal_version_id:
            continue
        # if dwi.deal_version_id in [43461, 43462]:
        #     print(dwi, dwi.status_before, dwi.status_after, dwi.comment)
        dv: DealVersion = DealVersion.objects.get(id=wfi.deal_version_id)
        if wfi.status_before is None and wfi.status_after == "DRAFT":
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.
        elif (
            wfi.status_before in ["REVIEW", "ACTIVATION"]
            and wfi.status_after == "DRAFT"
        ):
            # ic(
            #     "new draft... what to do?",
            #     wfi.timestamp,
            #     wfi.from_user,
            #     wfi.status_before,
            #     wfi.status_after
            # )
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.

        elif (wfi.status_before is None and wfi.status_after is None) or (
            wfi.status_before == wfi.status_after
        ):
            ...  # nothing?
        elif (
            wfi.status_before in [None, "DRAFT", "TO_DELETE"]
            and wfi.status_after == "REVIEW"
        ):
            dv.sent_to_review_at = wfi.timestamp
            dv.sent_to_review_by = wfi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
        elif (
            wfi.status_before in [None, "DRAFT", "REVIEW", "TO_DELETE"]
            and wfi.status_after == "ACTIVATION"
        ):
            dv.sent_to_activation_at = wfi.timestamp
            dv.sent_to_activation_by = wfi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
            # dv.status
        elif (
            wfi.status_before in ["REVIEW", "ACTIVATION"]
            and wfi.status_after == "ACTIVATED"
        ):
            dv.activated_at = wfi.timestamp
            dv.activated_by = wfi.from_user
            dv.save(recalculate_independent=False, recalculate_dependent=False)
        elif wfi.status_before == "ACTIVATION" and wfi.status_after == "REVIEW":
            pass  # ignoring this case because it's not changing anything on the deal
        elif wfi.status_before == "REJECTED" or wfi.status_after == "REJECTED":
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
            sys.exit(1)
        elif wfi.status_after == "TO_DELETE":
            dv.status = "DRAFT"
            dv.save(recalculate_independent=False, recalculate_dependent=False)
        elif wfi.status_before == "TO_DELETE" and wfi.status_after != "TO_DELETE":
            if not wfi.status_after:
                # TODO What is going on here?
                ...
            else:
                dv.status = status_map_dings[wfi.status_after]
                dv.save(recalculate_independent=False, recalculate_dependent=False)
        else:
            ...
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.to_user,
                wfi.deal_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
            # sys.exit(1)
