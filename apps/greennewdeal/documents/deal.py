import json

from django_elasticsearch import Document, fields
from django_elasticsearch.registries import registry
from geojson_rewind import rewind

from apps.greennewdeal.models import Contract, DataSource, Deal, Investor, Location


# noinspection PyMethodMayBeStatic
@registry.register_document
class DealDocument(Document):
    class Django:
        model = Deal
        related_models = [Location, Contract, DataSource]
        exclude = ["timestamp"]

        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000

    activity_identifier = fields.IntegerField(attr="id")

    def prepare_target_country(self, instance: Deal):
        if not instance.target_country:
            return None
        return {"id": instance.target_country.id, "name": instance.target_country.name}

    def prepare_purchase_price_currency(self, instance: Deal):
        if not instance.purchase_price_currency:
            return None
        return {
            "code": instance.purchase_price_currency.code,
            "name": instance.purchase_price_currency.name,
        }

    def prepare_annual_leasing_fee_currency(self, instance: Deal):
        if not instance.annual_leasing_fee_currency:
            return None
        return {
            "code": instance.annual_leasing_fee_currency.code,
            "name": instance.annual_leasing_fee_currency.name,
        }

    def prepare_operating_company(self, instance: Deal):
        oc: Investor = instance.operating_company
        if not oc:
            return None

        country_ret = region_ret = None

        country = oc.country
        if country:
            country_ret = {"id": country.id, "name": country.name}
            region = country.fk_region
            if region:
                region_ret = {"id": region.id, "name": region.name}

        return {
            "id": oc.id,
            "investor_identifier": oc.id,
            "name": oc.name,
            "country": country_ret,
            "region": region_ret,
            "classification": oc.classification,
            # "operating_company_classification": "10",
            # "operating_company_classification_display": "Private company",
            "homepage": oc.homepage,
            "comment": oc.comment,
            "timestamp": oc.timestamp,
            "opencorporates": oc.opencorporates,
        }

    def prepare_export_country1(self, instance: Deal):
        if not instance.export_country1:
            return None
        return {
            "id": instance.export_country1.id,
            "name": instance.export_country1.name,
        }

    def prepare_export_country2(self, instance: Deal):
        if not instance.export_country2:
            return None
        return {
            "id": instance.export_country2.id,
            "name": instance.export_country2.name,
        }

    def prepare_export_country3(self, instance: Deal):
        if not instance.export_country3:
            return None
        return {
            "id": instance.export_country3.id,
            "name": instance.export_country3.name,
        }

    locations = fields.NestedField(
        properties={
            "name": fields.TextField(),
            "point": fields.GeoPointField(),
            "intended_area": fields.GeoShapeField(),
            "production_area": fields.GeoShapeField(),
            "contract_area": fields.GeoShapeField(),
        }
    )
    geojson = fields.ObjectField()

    def prepare_geojson(self, instance: Deal):
        features = []
        for loc in instance.locations.all():  # type: Location
            if loc.point:
                point = {
                    "type": "Feature",
                    "geometry": (json.loads(loc.point.geojson)),
                    "properties": {"name": loc.name, "type": "point"},
                }
                features += [point]
            if loc.contract_area:
                contract_area = {
                    "type": "Feature",
                    "geometry": (json.loads(loc.contract_area.geojson)),
                    "properties": {"name": loc.name, "type": "contract_area"},
                }
                features += [rewind(contract_area)]
            if loc.intended_area:
                contract_area = {
                    "type": "Feature",
                    "geometry": (json.loads(loc.intended_area.geojson)),
                    "properties": {"name": loc.name, "type": "intended_area"},
                }
                features += [rewind(contract_area)]
            if loc.production_area:
                contract_area = {
                    "type": "Feature",
                    "geometry": (json.loads(loc.production_area.geojson)),
                    "properties": {"name": loc.name, "type": "production_area"},
                }
                features += [rewind(contract_area)]

        return {"type": "FeatureCollection", "features": features}

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Location):
            return related_instance.deal
        if isinstance(related_instance, Contract):
            return related_instance.deal
        if isinstance(related_instance, DataSource):
            return related_instance.deal

    class Index:
        name = "deal"


@registry.register_document
class LocationDocument(Document):
    def prepare_deal(self, instance: Location):
        deal = instance.deal
        return {
            "id": deal.id,
            "intended_size": deal.intended_size,
            # "contract_size": deal.contract_size,
            "implementation_status": deal.implementation_status,
        }

    class Django:
        model = Location
        exclude = ["old_group_id", "timestamp"]
        # ignore_signals = True

    class Index:
        name = "location"
