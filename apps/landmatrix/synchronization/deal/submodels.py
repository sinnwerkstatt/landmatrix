import json
import re

from django.contrib.gis.geos import Point
from geojson_rewind import rewind

from apps.landmatrix.synchronization.helpers import _to_nullbool, date_year_field


def create_locations(deal, groups, do_save, revision):
    ACCURACY_MAP = {
        None: "",
        "Country": "COUNTRY",
        "Administrative region": "ADMINISTRATIVE_REGION",
        "Región administrativa": "ADMINISTRATIVE_REGION",
        "Approximate location": "APPROXIMATE_LOCATION",
        "Ubicación aproximada": "APPROXIMATE_LOCATION",
        "Exact location": "EXACT_LOCATION",
        "Coordinates": "COORDINATES",
        "Coordenadas": "COORDINATES",
    }
    locations = []
    for group_id, attrs in sorted(groups.items()):
        location = {
            "old_group_id": group_id,
            "name": attrs.get("location") or "",
            "description": attrs.get("location_description") or "",
            "comment": attrs.get("tg_location_comment") or "",
            "facility_name": attrs.get("facility_name") or "",
            "level_of_accuracy": ACCURACY_MAP[attrs.get("level_of_accuracy")],
        }

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
                Point(point_lon, point_lat)
                location["point"] = {"lat": point_lat, "lng": point_lon}
            except:
                location["comment"] += (
                    f"\n\nWas unable to parse location."
                    f" The values are: lat:{point_lat} lon:{point_lon}"
                )
                location["point"] = None
        else:
            location["point"] = None

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

        location["areas"] = (
            {"type": "FeatureCollection", "features": features} if features else None
        )
        locations += [location]

    deal.locations = locations


def create_contracts(deal, groups, do_save, revision):
    # track former contracts, throw out the ones that still exist now, delete the rest
    # all_contracts = set(c.id for c in deal.contracts.all())
    contracts = []
    for group_id, attrs in sorted(groups.items()):
        contract = {
            "old_group_id": group_id,
            "number": attrs.get("contract_number") or "",
            "comment": attrs.get("tg_contract_comment") or "",
        }
        cdate = attrs.get("contract_date")
        if cdate:
            if date_year_field(cdate):
                contract["date"] = cdate
            else:
                raise Exception("!!")
        expdate = attrs.get("contract_expiration_date")
        if expdate:
            if date_year_field(expdate):
                contract["expiration_date"] = expdate
            else:
                raise Exception("!!")

        agreement_duration = attrs.get("agreement_duration")
        if agreement_duration == "99 years":
            agreement_duration = 99
        contract["agreement_duration"] = (
            int(agreement_duration) if agreement_duration else None
        )
        contracts += [contract]
    deal.contracts = contracts


def create_data_sources(deal, groups, do_save, revision):
    datasources = []

    TYPE_MAP = {
        None: "",
        "Media report": "MEDIA_REPORT",
        "Informe de prensa": "MEDIA_REPORT",
        "Research Paper / Policy Report": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Informe de Investigación/Informe de Políticas": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Government sources": "GOVERNMENT_SOURCES",
        "Fuentes gubernamentales": "GOVERNMENT_SOURCES",
        "Company sources": "COMPANY_SOURCES",
        "Fuentes empresariales": "COMPANY_SOURCES",
        "Contract": "CONTRACT",
        "Contract (contract farming agreement)": "CONTRACT_FARMING_AGREEMENT",
        "Personal information": "PERSONAL_INFORMATION",
        "Crowdsourcing": "CROWDSOURCING",
        "Other (Please specify in comment field)": "OTHER",
        "Otro (por favor, especifique en el campo para comentarios)": "OTHER",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    for group_id, attrs in sorted(groups.items()):

        url = attrs.get("url") or ""
        if url == "http%3A%2F%2Ffarmlandgrab.org%2F2510":
            url = "http://farmlandgrab.org/2510"

        ds = {
            "old_group_id": group_id,
            "type": TYPE_MAP[attrs.get("type")],
            "url": url,
            "file": f"uploads/{attrs.get('file')}" if attrs.get("file") else None,
            "file_not_public": attrs.get("file_not_public") == "True",
            "publication_title": attrs.get("publication_title") or "",
            "comment": attrs.get("tg_data_source_comment") or "",
            "name": attrs.get("name") or "",
            "company": attrs.get("company") or "",
            "email": attrs.get("email") or "",
            "phone": attrs.get("phone") or "",
            "includes_in_country_verified_information": _to_nullbool(
                attrs.get("includes_in_country_verified_information"),
            ),
            "open_land_contracts_id": attrs.get("open_land_contracts_id") or "",
        }

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

            if date_year_field(ds_date):
                ds["date"] = ds_date
            else:
                ds["comment"] += f"\n\nOld Date value: {ds_date}"
        else:
            ds["date"] = None
        datasources += [ds]
    deal.datasources = datasources
