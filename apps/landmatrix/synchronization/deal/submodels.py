import json
import re

from dateutil import parser
from django.contrib.gis.geos import Point
from geojson_rewind import rewind

from apps.landmatrix.models import Contract, DataSource, Location
from apps.landmatrix.synchronization.helpers import _to_nullbool


def create_locations(deal, groups):
    all_locations = set(c.id for c in deal.locations.all())

    ACCURACY_MAP = {
        None: None,
        "Country": "COUNTRY",
        "Administrative region": "ADMINISTRATIVE_REGION",
        "Approximate location": "APPROXIMATE_LOCATION",
        "Exact location": "EXACT_LOCATION",
        "Coordinates": "COORDINATES",
        "Coordenadas": "COORDINATES",
    }
    for group_id, attrs in sorted(groups.items()):
        try:
            location = Location.objects.get(deal=deal, old_group_id=group_id)
            all_locations.remove(location.id)
        except Location.DoesNotExist:
            location = Location(deal=deal, old_group_id=group_id)

        location.name = attrs.get("location") or ""
        location.description = attrs.get("location_description") or ""

        location.comment = attrs.get("tg_location_comment") or ""

        # location.point
        if attrs.get("point_lat") and attrs.get("point_lon"):
            try:
                point_lat = attrs.get("point_lat").replace(",", ".").replace("°", "")
                point_lat = float(point_lat)
            except ValueError:
                pass
            try:
                point_lon = attrs.get("point_lon").replace(",", ".").replace("°", "")
                point_lon = float(point_lon)
            except ValueError:
                pass
            try:
                location.point = Point(point_lon, point_lat)
            except:
                location.comment += f"\n\nWas unable to parse location. The values are: lat:{point_lat} lon:{point_lon}"
        else:
            location.point = None

        location.facility_name = attrs.get("facility_name") or ""
        location.level_of_accuracy = ACCURACY_MAP[attrs.get("level_of_accuracy")]

        features = []
        contract_area = attrs.get("contract_area", "polygon")
        intended_area = attrs.get("intended_area", "polygon")
        production_area = attrs.get("production_area", "polygon")
        if contract_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(contract_area.geojson)),
                "properties": {"type": "contract_area"},
            }
            features += [rewind(area_feature)]
        if intended_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(intended_area.geojson)),
                "properties": {"type": "intended_area"},
            }
            features += [rewind(area_feature)]
        if production_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(production_area.geojson)),
                "properties": {"type": "production_area"},
            }
            features += [rewind(area_feature)]

        location.areas = (
            {"type": "FeatureCollection", "features": features} if features else None
        )
        location.save()
    if all_locations:
        Location.objects.filter(id__in=all_locations).delete()


def create_contracts(deal, groups):
    all_contracts = set(c.id for c in deal.contracts.all())

    for group_id, attrs in sorted(groups.items()):
        try:
            contract = Contract.objects.get(deal=deal, old_group_id=group_id)
            all_contracts.remove(contract.id)
        except Contract.DoesNotExist:
            contract = Contract(deal=deal, old_group_id=group_id)

        contract.number = attrs.get("contract_number") or ""

        contract.date = (
            parser.parse(attrs.get("contract_date")).date()
            if attrs.get("contract_date")
            else None
        )

        contract.expiration_date = (
            parser.parse(attrs.get("contract_expiration_date")).date()
            if attrs.get("contract_expiration_date")
            else None
        )

        agreement_duration = attrs.get("agreement_duration")
        if agreement_duration == "99 years":
            agreement_duration = 99
        contract.agreement_duration = agreement_duration
        contract.comment = attrs.get("tg_contract_comment") or ""
        contract.save()
    if all_contracts:
        Contract.objects.filter(id__in=all_contracts).delete()


def create_data_sources(deal, groups):
    all_ds = set(c.id for c in deal.datasources.all())

    TYPE_MAP = {
        None: None,
        "Media report": "MEDIA_REPORT",
        "Research Paper / Policy Report": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Government sources": "GOVERNMENT_SOURCES",
        "Company sources": "COMPANY_SOURCES",
        "Contract": "CONTRACT",
        "Contract (contract farming agreement)": "CONTRACT_FARMING_AGREEMENT",
        "Personal information": "PERSONAL_INFORMATION",
        "Crowdsourcing": "CROWDSOURCING",
        "Other (Please specify in comment field)": "OTHER",
        "Other": "OTHER",
    }
    for group_id, attrs in sorted(groups.items()):
        try:
            data_source = DataSource.objects.get(deal=deal, old_group_id=group_id)
            all_ds.remove(data_source.id)
        except DataSource.DoesNotExist:
            data_source = DataSource(deal=deal, old_group_id=group_id)

        data_source.type = TYPE_MAP[attrs.get("type")]
        data_source.url = attrs.get("url")
        if attrs.get("file"):
            data_source.file.name = f"uploads/{attrs.get('file')}"
        else:
            data_source.file = None
        data_source.file_not_public = attrs.get("file_not_public") == "True"
        data_source.publication_title = attrs.get("publication_title") or ""

        data_source.comment = attrs.get("tg_data_source_comment") or ""

        ds_date = attrs.get("date")
        if ds_date:
            # NOTE Fixes for broken data
            if ":" in ds_date:
                ds_date = re.sub(
                    r"([0-9]{2}):([0-9]{2}):([0-9]{4})", r"\1.\2.\3", ds_date
                )
            broken_ds_dates = {
                "2019-18-02": "2019-02-18",
                "2014-29-09": "2014-09-29",
                "2017-02-29": "2017-02-28",
                "2018-11-31": "2018-11-30",
                "2019-28-05": "2019-05-28",
                "2019-04-31": "2019-04-30",
                "2018-17-04": "2018-04-17",
                "2020-15-11": "2020-11-15",
                "2017-17-01": "2017-01-17",
            }
            try:
                ds_date = broken_ds_dates[ds_date]
            except KeyError:
                pass

            try:
                data_source.date = parser.parse(ds_date).date()
            except:
                data_source.comment += f"\n\nOld Date value: {ds_date}"
        else:
            data_source.date = None
        data_source.name = attrs.get("name") or ""
        data_source.company = attrs.get("company") or ""
        data_source.email = attrs.get("email") or ""
        data_source.phone = attrs.get("phone") or ""
        data_source.includes_in_country_verified_information = _to_nullbool(
            attrs.get("includes_in_country_verified_information")
        )
        data_source.open_land_contracts_id = attrs.get("open_land_contracts_id") or ""
        data_source.save()
    if all_ds:
        DataSource.objects.filter(id__in=all_ds).delete()
