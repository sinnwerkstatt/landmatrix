from datetime import datetime

from django.contrib.gis.geos import Point

from apps.greennewdeal.models import Contract, DataSource, Location


def create_locations(deal, groups):
    ACCURACY_MAP = {
        None: None,
        "Country": 50,
        "Administrative region": 40,
        "Approximate location": 30,
        "Exact location": 20,
        "Coordinates": 10,
    }
    for group_id, attrs in sorted(groups.items()):
        try:
            location = Location.objects.get(deal=deal, old_group_id=group_id)
        except Location.DoesNotExist:
            location = Location(deal=deal, old_group_id=group_id)

        location.name = attrs.get("location") or ""
        if attrs.get("point_lat") and attrs.get("point_lon"):
            loc_point_lat = float(attrs.get("point_lat"))
            loc_point_lon = float(attrs.get("point_lon"))
            location.point = Point(loc_point_lon, loc_point_lat)
        location.description = attrs.get("location_description") or ""
        location.facility_name = attrs.get("facility_name") or ""

        location.level_of_accuracy = ACCURACY_MAP[attrs.get("level_of_accuracy")]
        location.comment = attrs.get("tg_location_comment") or ""
        location.contract_area = attrs.get("contract_area", "polygon")
        location.intended_area = attrs.get("intended_area", "polygon")
        location.production_area = attrs.get("production_area", "polygon")
        location.save()


def create_contracts(deal, groups):
    for group_id, attrs in sorted(groups.items()):
        try:
            contract = Contract.objects.get(deal=deal, old_group_id=group_id)
        except Contract.DoesNotExist:
            contract = Contract(deal=deal, old_group_id=group_id)

        contract.number = attrs.get("contract_number") or ""
        if attrs.get("contract_date"):
            contract.date = datetime.strptime(attrs.get("contract_date"), "%Y-%m-%d")
        if attrs.get("contract_expiration_date"):
            contract.date = datetime.strptime(
                attrs.get("contract_expiration_date"), "%Y-%m-%d"
            )
        contract.agreement_duration = attrs.get("agreement_duration")
        contract.comment = attrs.get("tg_contract_comment") or ""
        contract.save()


def create_data_sources(deal, groups):
    TYPE_MAP = {
        None: None,
        "Media report": 10,
        "Research Paper / Policy Report": 20,
        "Government sources": 30,
        "Company sources": 40,
        "Contract": 50,
        "Contract (contract farming agreement)": 60,
        "Personal information": 70,
        "Crowdsourcing": 80,
        "Other (Please specify in comment field)": 90,
        "Other": 90,
    }
    for group_id, attrs in sorted(groups.items()):
        try:
            data_source = DataSource.objects.get(deal=deal, old_group_id=group_id)
        except DataSource.DoesNotExist:
            data_source = DataSource(deal=deal, old_group_id=group_id)

        data_source.type = TYPE_MAP[attrs.get("type")]
        data_source.url = attrs.get("url")
        if attrs.get("file"):
            data_source.file.name = f"uploads/{attrs.get('file')}"
        data_source.file_not_public = attrs.get("file_not_public") == "True"
        data_source.publication_title = attrs.get("publication_title") or ""
        data_source.date = attrs.get("date")
        data_source.name = attrs.get("name") or ""
        data_source.company = attrs.get("company") or ""
        data_source.email = attrs.get("email") or ""
        data_source.phone = attrs.get("phone") or ""
        data_source.includes_in_country_verified_information = (
            attrs.get("includes_in_country_verified_information") == "True"
        )
        data_source.open_land_contracts_id = attrs.get("open_land_contracts_id") or ""
        data_source.comment = attrs.get("tg_data_source_comment") or ""
        data_source.save()
