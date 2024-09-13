import json
from enum import Enum
from typing import Any

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.contrib.gis.geos.prototypes.io import wkt_w
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import Count, Func, F, Q
from django.http import Http404
from django.utils.translation import gettext as _
from nanoid import generate

from apps.accounts.models import User
from apps.landmatrix.models import schema, choices
from apps.landmatrix.models.abstract import (
    BaseHull,
    BaseVersion,
    VersionTransition,
    VersionStatus,
    BaseDataSource,
    BaseWorkflowInfo,
)
from apps.landmatrix.models.choices import (
    NegotiationStatusEnum,
    ImplementationStatusEnum,
    NatureOfDealEnum,
    IntentionOfInvestmentEnum,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.fields import (
    ChoiceArrayField,
    ArrayField,
    NanoIDField,
    LooseDateField,
)
from apps.landmatrix.models.investor import InvestorHull
from apps.landmatrix.nid import generate_nid
from django_pydantic_jsonfield import PydanticJSONField, SchemaValidator


class DealHullQuerySet(models.QuerySet):
    def normal(self):
        return self.filter(deleted=False)

    def active(self):
        return self.normal().filter(active_version__isnull=False)

    def public(self):
        return self.active().filter(active_version__is_public=True, confidential=False)

    def visible(self, user=None, subset="PUBLIC"):
        # TODO Later: welche user duerfen unfiltered bekommen?
        if not user or not user.is_authenticated:
            return self.public()

        if subset == "PUBLIC":
            return self.public()
        elif subset == "ACTIVE":
            return self.active()
        return self.normal()

    # def with_mode(self):
    #     return self.annotate(
    #         mode=Case(
    #             When(
    #                 ~Q(active_version_id=None) & ~Q(draft_version_id=None),
    #                 then=Concat(Value("ACTIVE + "), "draft_version__status"),
    #             ),
    #             When(
    #                 ~Q(active_version_id=None) & Q(draft_version_id=None),
    #                 then=Value("ACTIVE"),
    #             ),
    #             When(
    #                 Q(active_version_id=None) & ~Q(draft_version_id=None),
    #                 then="draft_version__status",
    #             ),
    #             default=Value(""),
    #         )
    #     )


class DealHull(BaseHull):
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deals",
    )

    active_version = models.ForeignKey(
        "DealVersion",
        verbose_name=_("Active version"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        "DealVersion",
        verbose_name=_("Draft version"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    confidential = models.BooleanField(
        _("Confidential"),
        default=False,
    )
    confidential_comment = models.TextField(
        _("Comment why this deal is private"),
        blank=True,
    )

    # ## calculated
    fully_updated_at = models.DateTimeField(
        _("Last full update"),
        blank=True,
        null=True,
    )

    objects = DealHullQuerySet.as_manager()

    def __str__(self):
        if self.country:
            return f"#{self.id} in {self.country.name}"
        return f"#{self.id}"

    def selected_version(self):
        if hasattr(self, "_selected_version_id") and self._selected_version_id:

            try:
                return self.versions.get(id=self._selected_version_id)
            except DealVersion.DoesNotExist:
                raise Http404
        return self.active_version or self.draft_version

    def add_draft(self, created_by: User = None) -> "DealVersion":
        dv = DealVersion.objects.create(
            deal=self,
            created_by=created_by,
            modified_by=created_by,
        )
        self.draft_version = dv
        self.save()
        return dv

    @classmethod
    def get_geo_markers(cls, region_id=None, country_id=None):
        deals = cls.objects.public().exclude(country=None)
        if region_id:
            return [
                {
                    "country_id": x["country_id"],
                    "count": x["count"],
                    "coordinates": [x["country__point_lat"], x["country__point_lon"]],
                }
                for x in deals.filter(country__region_id=region_id)
                .values("country_id", "country__point_lat", "country__point_lon")
                .annotate(count=Count("pk"))
                # .annotate(size=Sum("deal_size"))
            ]
        if country_id:
            xx = [
                {"coordinates": x}
                for x in deals.filter(country_id=country_id)
                .filter(active_version__locations__point__isnull=False)
                .annotate(
                    point_lat=Func(
                        "active_version__locations__point",
                        function="ST_Y",
                        output_field=models.FloatField(),
                    ),
                    point_lng=Func(
                        "active_version__locations__point",
                        function="ST_X",
                        output_field=models.FloatField(),
                    ),
                )
                .values_list("point_lat", "point_lng")
            ]
            return xx

        region_coordinates = {
            2: [6.06433, 17.082249],
            9: [-22.7359, 140.0188],
            21: [54.526, -105.2551],
            142: [34.0479, 100.6197],
            150: [52.0055, 37.9587],
            419: [-4.442, -61.3269],
        }
        return [
            {
                "region_id": x["region_id"],
                "count": x["count"],
                "coordinates": region_coordinates[x["region_id"]],
            }
            for x in deals.values(region_id=F("country__region_id")).annotate(
                count=Count("pk")
            )
        ]


class DealVersionBaseFields(models.Model):
    deal = models.ForeignKey(
        DealHull,
        verbose_name=_("Deal"),
        on_delete=models.PROTECT,
        related_name="versions",
    )

    # """ Locations """
    # via Foreignkey

    """ General info """
    # Land area
    intended_size = models.DecimalField(
        _("Intended size"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contract_size = PydanticJSONField(
        _("Contract size"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateAreaSchema)],
    )
    production_size = PydanticJSONField(
        _("Production size"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateAreaSchema)],
    )
    land_area_comment = models.TextField(
        _("Comment on land area"),
        blank=True,
    )

    # Intention of investment
    intention_of_investment = PydanticJSONField(
        _("Intention of investment"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateAreaChoicesIOI)],
    )
    intention_of_investment_comment = models.TextField(
        _("Comment on intention of investment"),
        blank=True,
    )

    # Carbon offset project
    carbon_offset_project = models.BooleanField(
        _("Carbon offset project"),
        blank=True,
        null=True,
    )
    carbon_offset_project_comment = models.TextField(
        _("Comment on carbon offset project"),
        blank=True,
    )

    # Nature of the deal
    nature_of_deal = ChoiceArrayField(
        models.CharField(choices=choices.NATURE_OF_DEAL_CHOICES),
        verbose_name=_("Nature of the deal"),
        blank=True,
        default=list,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"),
        blank=True,
    )

    # # Negotiation status
    negotiation_status = PydanticJSONField(
        _("Negotiation status"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateChoiceNegotiationStatus)],
    )
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"),
        blank=True,
    )

    # # Implementation status
    implementation_status = PydanticJSONField(
        _("Implementation status"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateChoiceImplementationStatus)],
    )
    implementation_status_comment = models.TextField(
        _("Comment on implementation status"),
        blank=True,
    )

    # Purchase price
    purchase_price = models.DecimalField(
        _("Purchase price"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    purchase_price_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Purchase price currency"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    purchase_price_type = models.CharField(
        _("Purchase price area type"),
        choices=choices.HA_AREA_CHOICES,
        blank=True,
        null=True,
    )
    purchase_price_area = models.DecimalField(
        _("Purchase price area"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    purchase_price_comment = models.TextField(
        _("Comment on purchase price"),
        blank=True,
    )

    # Leasing fees
    annual_leasing_fee = models.DecimalField(
        _("Annual leasing fee"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    annual_leasing_fee_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Annual leasing fee currency"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    annual_leasing_fee_type = models.CharField(
        _("Annual leasing fee area type"),
        choices=choices.HA_AREA_CHOICES,
        blank=True,
        null=True,
    )
    annual_leasing_fee_area = models.DecimalField(
        _("Annual leasing fee area"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    annual_leasing_fee_comment = models.TextField(
        _("Comment on leasing fee"),
        blank=True,
    )

    # Contract farming
    contract_farming = models.BooleanField(
        _("Contract farming"),
        blank=True,
        null=True,
    )
    on_the_lease_state = models.BooleanField(
        _("On leased / purchased"),
        blank=True,
        null=True,
    )
    on_the_lease = PydanticJSONField(
        _("On leased area/farmers/households"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.LeaseSchema)],
    )
    off_the_lease_state = models.BooleanField(
        _("Not on leased / purchased (out-grower)"),
        blank=True,
        null=True,
    )
    off_the_lease = PydanticJSONField(
        _("Not on leased area/farmers/households (out-grower)"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.LeaseSchema)],
    )
    contract_farming_comment = models.TextField(
        _("Comment on contract farming"),
        blank=True,
    )

    # """ Contracts """
    # via Foreignkey

    """ Employment """
    total_jobs_created = models.BooleanField(
        _("Jobs created (total)"),
        blank=True,
        null=True,
    )
    total_jobs_planned = models.IntegerField(
        _("Planned number of jobs (total)"),
        blank=True,
        null=True,
    )
    total_jobs_planned_employees = models.IntegerField(
        _("Planned employees (total)"),
        blank=True,
        null=True,
    )
    total_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (total)"),
        blank=True,
        null=True,
    )
    total_jobs_current = PydanticJSONField(
        _("Current total number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.JobsSchema)],
    )
    total_jobs_created_comment = models.TextField(
        _("Comment on jobs created (total)"),
        blank=True,
    )

    foreign_jobs_created = models.BooleanField(
        _("Jobs created (foreign)"),
        blank=True,
        null=True,
    )
    foreign_jobs_planned = models.IntegerField(
        _("Planned number of jobs (foreign)"),
        blank=True,
        null=True,
    )
    foreign_jobs_planned_employees = models.IntegerField(
        _("Planned employees (foreign)"),
        blank=True,
        null=True,
    )
    foreign_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (foreign)"),
        blank=True,
        null=True,
    )
    foreign_jobs_current = PydanticJSONField(
        _("Current foreign number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.JobsSchema)],
    )
    foreign_jobs_created_comment = models.TextField(
        _("Comment on jobs created (foreign)"),
        blank=True,
    )

    domestic_jobs_created = models.BooleanField(
        _("Jobs created (domestic)"),
        blank=True,
        null=True,
    )
    domestic_jobs_planned = models.IntegerField(
        _("Planned number of jobs (domestic)"),
        blank=True,
        null=True,
    )
    domestic_jobs_planned_employees = models.IntegerField(
        _("Planned employees (domestic)"),
        blank=True,
        null=True,
    )
    domestic_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (domestic)"),
        blank=True,
        null=True,
    )
    domestic_jobs_current = PydanticJSONField(
        _("Current domestic number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.JobsSchema)],
    )
    domestic_jobs_created_comment = models.TextField(
        _("Comment on jobs created (domestic)"),
        blank=True,
    )

    """ Investor info """
    operating_company = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Operating company"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dealversions",
    )
    involved_actors = PydanticJSONField(
        _("Actors involved in the negotiation / admission process"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.ActorsSchema)],
    )
    project_name = models.CharField(
        _("Name of investment project"),
        blank=True,
    )
    investment_chain_comment = models.TextField(
        _("Comment on investment chain"),
        blank=True,
    )

    # """ Data sources """  via Foreignkey

    """ Local communities / indigenous peoples """
    name_of_community = ArrayField(
        models.CharField(),
        verbose_name=_("Name of community"),
        blank=True,
        default=list,
    )
    name_of_indigenous_people = ArrayField(
        models.CharField(),
        verbose_name=_("Name of indigenous people"),
        blank=True,
        default=list,
    )
    people_affected_comment = models.TextField(
        _("Comment on communities / indigenous peoples affected"),
        blank=True,
    )

    recognition_status = ChoiceArrayField(
        models.CharField(choices=choices.RECOGNITION_STATUS_CHOICES),
        verbose_name=_("Recognition status of community land tenure"),
        blank=True,
        default=list,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognition status of community land tenure"),
        blank=True,
    )
    community_consultation = models.CharField(
        _("Community consultation"),
        choices=choices.COMMUNITY_CONSULTATION_CHOICES,
        blank=True,
        null=True,
    )
    community_consultation_comment = models.TextField(
        _("Comment on consultation of local community"),
        blank=True,
    )

    community_reaction = models.CharField(
        _("Community reaction"),
        choices=choices.COMMUNITY_REACTION_CHOICES,
        blank=True,
        null=True,
    )
    community_reaction_comment = models.TextField(
        _("Comment on community reaction"),
        blank=True,
    )

    land_conflicts = models.BooleanField(
        _("Presence of land conflicts"),
        blank=True,
        null=True,
    )
    land_conflicts_comment = models.TextField(
        _("Comment on presence of land conflicts"),
        blank=True,
    )

    displacement_of_people = models.BooleanField(
        _("Displacement of people"),
        blank=True,
        null=True,
    )
    displaced_people = models.IntegerField(
        _("Number of people actually displaced"),
        blank=True,
        null=True,
    )
    displaced_households = models.IntegerField(
        _("Number of households actually displaced"),
        blank=True,
        null=True,
    )
    displaced_people_from_community_land = models.IntegerField(
        _("Number of people displaced out of their community land"),
        blank=True,
        null=True,
    )
    displaced_people_within_community_land = models.IntegerField(
        _("Number of people displaced staying on community land"),
        blank=True,
        null=True,
    )
    displaced_households_from_fields = models.IntegerField(
        _('Number of households displaced "only" from their agricultural fields'),
        blank=True,
        null=True,
    )
    displaced_people_on_completion = models.IntegerField(
        _("Number of people facing displacement once project is fully implemented"),
        blank=True,
        null=True,
    )
    displacement_of_people_comment = models.TextField(
        _("Comment on displacement of people"),
        blank=True,
    )

    negative_impacts = ChoiceArrayField(
        models.CharField(choices=choices.NEGATIVE_IMPACTS_CHOICES),
        verbose_name=_("Negative impacts for local communities"),
        blank=True,
        default=list,
    )
    negative_impacts_comment = models.TextField(
        _("Comment on negative impacts for local communities"),
        blank=True,
    )

    promised_compensation = models.TextField(
        _("Promised compensation (e.g. for damages or resettlements)"),
        blank=True,
    )
    received_compensation = models.TextField(
        _("Received compensation (e.g. for damages or resettlements)"),
        blank=True,
    )

    promised_benefits = ChoiceArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Promised benefits for local communities"),
        blank=True,
        default=list,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"),
        blank=True,
    )

    materialized_benefits = ChoiceArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Materialized benefits for local communities"),
        blank=True,
        default=list,
    )
    materialized_benefits_comment = models.TextField(
        _("Comment on materialized benefits for local communities"),
        blank=True,
    )

    presence_of_organizations = models.TextField(
        _(
            "Presence of organizations and actions taken "
            "(e.g. farmer organizations, NGOs, etc.)"
        ),
        blank=True,
    )

    """ Former use """
    former_land_owner = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_OWNER_CHOICES),
        verbose_name=_("Former land owner"),
        blank=True,
        default=list,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"),
        blank=True,
    )
    former_land_use = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_USE_CHOICES),
        verbose_name=_("Former land use"),
        blank=True,
        default=list,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"),
        blank=True,
    )
    former_land_cover = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_COVER_CHOICES),
        verbose_name=_("Former land cover"),
        blank=True,
        default=list,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"),
        blank=True,
    )

    """ Produce info """
    crops = PydanticJSONField(
        _("Crops area/yield/export"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.ExportsCrops)],
    )
    crops_comment = models.TextField(
        _("Comment on crops"),
        blank=True,
    )

    animals = PydanticJSONField(
        _("Livestock area/yield/export"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.ExportsAnimals)],
    )
    animals_comment = models.TextField(
        _("Comment on livestock"),
        blank=True,
    )

    mineral_resources = PydanticJSONField(
        _("Mineral resources area/yield/export"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.ExportsMineralResources)],
    )
    mineral_resources_comment = models.TextField(
        _("Comment on mineral resources"),
        blank=True,
    )

    contract_farming_crops = PydanticJSONField(
        _("Contract farming crops"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateAreaChoicesCrops)],
    )
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"),
        blank=True,
    )

    contract_farming_animals = PydanticJSONField(
        _("Contract farming livestock"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CurrentDateAreaChoicesAnimals)],
    )
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"),
        blank=True,
    )

    electricity_generation = PydanticJSONField(
        _("Electricity generation"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.ElectricityGenerationSchema)],
    )
    electricity_generation_comment = models.TextField(
        _("Comment on electricity generation"),
        blank=True,
    )

    carbon_sequestration = PydanticJSONField(
        _("Carbon sequestration/offsetting"),
        blank=True,
        default=list,
        validators=[SchemaValidator(schema.CarbonSequestrationSchema)],
    )
    carbon_sequestration_comment = models.TextField(
        _("Comment on carbon sequestration/offsetting"),
        blank=True,
    )

    has_domestic_use = models.BooleanField(
        _("Has domestic use"),
        blank=True,
        null=True,
    )
    domestic_use = models.FloatField(
        _("Domestic use"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    has_export = models.BooleanField(
        _("Has export"),
        blank=True,
        null=True,
    )
    export = models.FloatField(
        _("Export"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    export_country1 = models.ForeignKey(
        Country,
        verbose_name=_("Country 1"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country1_ratio = models.FloatField(
        _("Country 1 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country2 = models.ForeignKey(
        Country,
        verbose_name=_("Country 2"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country2_ratio = models.FloatField(
        _("Country 2 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country3 = models.ForeignKey(
        Country,
        verbose_name=_("Country 3"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country3_ratio = models.FloatField(
        _("Country 3 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    use_of_produce_comment = models.TextField(
        verbose_name=_("Comment on use of produce"),
        blank=True,
    )

    in_country_processing = models.BooleanField(
        _("In country processing of produce"),
        blank=True,
        null=True,
    )
    in_country_processing_comment = models.TextField(
        _("Comment on in country processing of produce"),
        blank=True,
    )
    in_country_processing_facilities = models.TextField(
        _(
            "Processing facilities / production infrastructure of the project "
            "(e.g. oil mill, ethanol distillery, biomass power plant etc.)"
        ),
        blank=True,
    )
    in_country_end_products = models.TextField(
        _("In-country end products of the project"),
        blank=True,
    )

    """Water"""
    water_extraction_envisaged = models.BooleanField(
        _("Water extraction envisaged"),
        blank=True,
        null=True,
    )
    water_extraction_envisaged_comment = models.TextField(
        _("Comment on water extraction envisaged"),
        blank=True,
    )

    source_of_water_extraction = ChoiceArrayField(
        models.CharField(choices=choices.WATER_SOURCE_CHOICES),
        verbose_name=_("Source of water extraction"),
        blank=True,
        default=list,
    )
    source_of_water_extraction_comment = models.TextField(
        _("Comment on source of water extraction"),
        blank=True,
    )
    how_much_do_investors_pay_comment = models.TextField(
        _("Comment on how much do investors pay for water"),
        blank=True,
    )

    water_extraction_amount = models.IntegerField(
        _("Water extraction amount"),
        blank=True,
        null=True,
    )
    water_extraction_amount_comment = models.TextField(
        _("Comment on how much water is extracted"),
        blank=True,
    )
    use_of_irrigation_infrastructure = models.BooleanField(
        _("Use of irrigation infrastructure"),
        blank=True,
        null=True,
    )
    use_of_irrigation_infrastructure_comment = models.TextField(
        _("Comment on use of irrigation infrastructure"),
        blank=True,
    )
    water_footprint = models.TextField(
        _("Water footprint of the investment project"),
        blank=True,
    )

    """ Gender-related info """
    gender_related_information = models.TextField(
        _("Comment on gender-related info"),
        blank=True,
    )

    """ Overall comment """
    overall_comment = models.TextField(
        _("Overall comment"),
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ("id",)


class DealVersion(DealVersionBaseFields, BaseVersion):
    """# CALCULATED FIELDS #"""

    # is_public: change the logic how it's calculated a bit - confidential is dealhull stuff
    is_public = models.BooleanField(
        _("Is public"),
        default=False,
    )
    has_known_investor = models.BooleanField(
        _("Has known investor"),
        default=False,
    )

    # NOTE: Next two fields should have used through keyword.
    parent_companies = models.ManyToManyField(
        InvestorHull,
        verbose_name=_("Parent companies"),
        related_name="child_deals",
        blank=True,
    )
    # Can be queried via DealTopInvestors view model:
    top_investors = models.ManyToManyField(
        InvestorHull,
        verbose_name=_("Top parent companies"),
        related_name="+",
        blank=True,
    )
    current_contract_size = models.DecimalField(
        _("Current contract size"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_production_size = models.DecimalField(
        _("Current production size"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_intention_of_investment = ChoiceArrayField(
        models.CharField(choices=choices.INTENTION_OF_INVESTMENT_CHOICES),
        verbose_name=_("Current intention of investment"),
        blank=True,
        default=list,
    )
    current_negotiation_status = models.CharField(
        _("Current negotiation status"),
        choices=choices.NEGOTIATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    current_implementation_status = models.CharField(
        _("Current implementation status"),
        choices=choices.IMPLEMENTATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    current_crops = ArrayField(
        models.CharField(),
        verbose_name=_("Current crops"),
        blank=True,
        default=list,
    )
    current_animals = ArrayField(
        models.CharField(),
        verbose_name=_("Current livestock"),
        blank=True,
        default=list,
    )
    current_mineral_resources = ArrayField(
        models.CharField(),
        verbose_name=_("Current mineral resources"),
        blank=True,
        default=list,
    )
    current_electricity_generation = ArrayField(
        models.CharField(),
        verbose_name=_("Current electricity generation"),
        blank=True,
        default=list,
    )
    current_carbon_sequestration = ArrayField(
        models.CharField(),
        verbose_name=_("Current carbon sequestration/offsetting"),
        blank=True,
        default=list,
    )

    deal_size = models.DecimalField(
        _("Deal size"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    initiation_year = models.IntegerField(
        _("Initiation year"),
        blank=True,
        null=True,
        validators=[MinValueValidator(1970)],
    )
    forest_concession = models.BooleanField(
        _("Forest concession"),
        default=False,
    )
    transnational = models.BooleanField(
        _("Transnational"),
        blank=True,
        null=True,
    )

    # META
    fully_updated = models.BooleanField(
        _("Fully updated"),
        default=False,
    )

    def __str__(self):
        return f"v{self.id} for #{self.deal_id}"

    def is_current_draft(self):
        return self.deal.draft_version_id == self.id

    @transaction.atomic
    def save(
        self,
        recalculate_independent=True,
        recalculate_dependent=True,
        *args,
        **kwargs,
    ):
        self._recalculate_fields(recalculate_independent, recalculate_dependent)
        super().save(*args, **kwargs)

    def _recalculate_fields(self, independent=True, dependent=True):
        if independent:
            self.current_contract_size = self.__get_current(self.contract_size, "area")
            self.current_production_size = self.__get_current(
                self.production_size, "area"
            )
            self.current_intention_of_investment = (
                self.__get_current(self.intention_of_investment, "choices", multi=True)
                or []
            )
            self.current_negotiation_status = self.__get_current(
                self.negotiation_status, "choice"
            )
            self.current_implementation_status = self.__get_current(
                self.implementation_status, "choice"
            )
            self.current_crops = (
                self.__get_current(self.crops, "choices", multi=True) or []
            )
            self.current_animals = (
                self.__get_current(self.animals, "choices", multi=True) or []
            )
            self.current_mineral_resources = (
                self.__get_current(self.mineral_resources, "choices", multi=True) or []
            )
            self.current_electricity_generation = (
                self.__get_current(self.electricity_generation, "choices", multi=True)
                or []
            )
            self.current_carbon_sequestration = (
                self.__get_current(self.carbon_sequestration, "choices", multi=True)
                or []
            )

            # these only depend on the __get_current calls right above.
            self.deal_size = self.__calculate_deal_size()
            self.initiation_year = self.__calculate_initiation_year()
            self.forest_concession = self.__calculate_forest_concession()
        if dependent:
            # With the help of signals these fields are recalculated on changes to:
            # Investor and InvestorVentureInvolvement
            self.has_known_investor = self.__has_known_investor()
            self.is_public = self.__calculate_is_public()

            # this might error because it's m2m, and we need the
            # Deal to have an ID first before we can save the investors. 🙄
            self.__calculate_parent_companies()
            self.transnational = self.__calculate_transnational()

    def change_status(
        self,
        transition: VersionTransition,
        user: User,
        fully_updated=False,
        to_user_id: int = None,
        comment="",
    ):
        old_draft_status = self.status

        super().change_status(transition=transition, user=user, to_user_id=to_user_id)

        if transition == VersionTransition.TO_REVIEW:
            if fully_updated:
                self.fully_updated = True
            self.save()

        elif transition == VersionTransition.ACTIVATE:
            deal = self.deal
            deal.draft_version = None
            deal.active_version = self
            # using "last modified" timestamp for "last fully updated" #681
            if self.fully_updated:
                deal.fully_updated_at = self.modified_at
            deal.save()

            # close unresolved workflowinfos
            self.workflowinfos.all().update(resolved=True)

        elif transition == VersionTransition.TO_DRAFT:
            self.save()

            deal = self.deal
            deal.draft_version = self
            deal.save()

            # close remaining open feedback requests
            self.workflowinfos.filter(
                Q(
                    status_before__in=[
                        VersionStatus.REVIEW,
                        VersionStatus.ACTIVATION,
                    ]
                )
                & Q(status_after=VersionStatus.DRAFT)
                & (Q(from_user=user) | Q(to_user=user))
            ).update(resolved=True)

        # TODO: Factor out

        DealWorkflowInfo.objects.create(
            deal_id=self.deal_id,
            deal_version=self,
            from_user=user,
            to_user_id=to_user_id if user.id != to_user_id else None,
            status_before=old_draft_status,
            status_after=self.status,
            comment=comment,
        )

    def copy_to_new_draft(self, created_by_id: int):
        old_self = DealVersion.objects.get(pk=self.pk)
        super().copy_to_new_draft(created_by_id)
        self.save()

        # copy foreignkey-relations
        for l1 in old_self.locations.all():
            l1.id = None
            l1.dealversion = self
            l1.save()

            for a1 in l1.areas.all():
                a1.id = None
                a1.location = l1
                a1.save()

        for d1 in old_self.datasources.all():
            d1.id = None
            d1.dealversion = self
            d1.save()

        for c1 in old_self.contracts.all():
            c1.id = None
            c1.dealversion = self
            c1.save()

        self.save()

    @staticmethod
    def __get_current(attributes, field, multi=False):
        if not attributes:
            return None

        def get_value_safe(val: Any) -> Any:
            # probably not needed any more...
            return val.value if isinstance(val, Enum) else val

        if multi:
            values = [
                get_value_safe(val)
                for attr in attributes
                for val in attr.get(field, [])
                if attr.get("current")
            ]
            return values or None

        values = [attr.get(field) for attr in attributes if attr.get("current")]

        if values:
            return get_value_safe(values[0])
        else:
            raise ValidationError('At least one value needs to be "current".')

    def __calculate_parent_companies(self) -> None:
        from apps.landmatrix.models.investor import InvestorHull

        if self.operating_company_id:
            oc: InvestorHull | None = (
                InvestorHull.objects.active()
                .filter(id=self.operating_company_id)
                .first()
            )
            if oc:
                parent_companies = oc.get_parent_companies()
                self.parent_companies.set(parent_companies)
                top_inv = [x for x in parent_companies if x.is_top_investor]
                self.top_investors.set(top_inv)
                return
        if self.id:
            self.parent_companies.set([])
            self.top_investors.set([])

    def __calculate_is_public(self) -> bool:
        if not self.id or not self.datasources.count():
            # No DataSource
            return False
        if not self.operating_company_id:
            # 3. No operating company
            return False
        if not self.has_known_investor:
            # 4. Unknown operating company AND no known operating company parents
            return False
        return True

    def __has_known_investor(self) -> bool:
        from apps.landmatrix.models.investor import InvestorHull

        if not self.operating_company_id:
            return False
        try:
            oc = InvestorHull.objects.active().get(id=self.operating_company_id)
        except InvestorHull.DoesNotExist:
            return False

        if not oc.active_version.name_unknown:
            return True

        # see if one of the parents of the investor exists
        if oc.parent_investors.filter(
            parent_investor__active_version__name_unknown=False
        ).exists():
            return True

        return False

    def __calculate_deal_size(self):
        negotiation_status = self.current_negotiation_status
        if not negotiation_status:
            return 0

        intended_size = self.intended_size or 0.0
        contract_size = self.current_contract_size or 0.0
        production_size = self.current_production_size or 0.0

        if negotiation_status in (
            NegotiationStatusEnum.EXPRESSION_OF_INTEREST,
            NegotiationStatusEnum.UNDER_NEGOTIATION,
            NegotiationStatusEnum.MEMORANDUM_OF_UNDERSTANDING,
            ## Failed
            NegotiationStatusEnum.NEGOTIATIONS_FAILED,
        ):
            value = intended_size or contract_size or production_size
        elif negotiation_status in (
            NegotiationStatusEnum.ORAL_AGREEMENT,
            NegotiationStatusEnum.CONTRACT_SIGNED,
            NegotiationStatusEnum.CHANGE_OF_OWNERSHIP,
            ## Canceled or Expired
            NegotiationStatusEnum.CONTRACT_CANCELED,
            NegotiationStatusEnum.CONTRACT_EXPIRED,
        ):
            value = contract_size or production_size
        else:
            # This should not happen
            value = 0.0
        return value

    def __calculate_initiation_year(self):
        def year_as_int(date: str) -> int:
            return int(date[:4])

        negotiation_status_dates = [
            x["date"]
            for x in self.negotiation_status
            if x.get("date")
            and x.get("choice")
            in (
                NegotiationStatusEnum.UNDER_NEGOTIATION,
                NegotiationStatusEnum.ORAL_AGREEMENT,
                NegotiationStatusEnum.CONTRACT_SIGNED,
                NegotiationStatusEnum.NEGOTIATIONS_FAILED,
                NegotiationStatusEnum.CONTRACT_CANCELED,
            )
        ]

        implementation_status_dates = [
            x["date"]
            for x in self.implementation_status
            if x.get("date")
            and x.get("choice")
            in (
                ImplementationStatusEnum.STARTUP_PHASE,
                ImplementationStatusEnum.IN_OPERATION,
                ImplementationStatusEnum.PROJECT_ABANDONED,
            )
        ]

        dates = implementation_status_dates + negotiation_status_dates

        return min([year_as_int(d) for d in dates]) if dates else None

    def __calculate_forest_concession(self) -> bool:
        is_concession = NatureOfDealEnum.CONCESSION in (self.nature_of_deal or [])
        is_forest_logging = IntentionOfInvestmentEnum.FOREST_LOGGING in (
            self.current_intention_of_investment or []
        )
        return is_concession and is_forest_logging

    def __calculate_transnational(self) -> bool | None:
        if not self.deal.country_id:
            # unknown if we have no target country
            return None

        # by definition True, if no operating company exists (or it is deleted)
        if not self.operating_company_id:
            return True
        if self.operating_company.deleted:
            return True

        investors_countries = self.parent_companies.exclude(
            active_version__country_id=None
        ).values_list("active_version__country_id", flat=True)

        if not len(investors_countries):
            # treat deals without investors as transnational
            # treat deals without investor countries as transnational
            return True
        # `True` if we have investors in other countries else `False`
        return bool(set(investors_countries) - {self.deal.country_id})


class Location(models.Model):
    dealversion = models.ForeignKey(
        DealVersion,
        on_delete=models.CASCADE,
        related_name="locations",
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    level_of_accuracy = models.CharField(
        _("Spatial accuracy level"),
        blank=True,
        choices=choices.LOCATION_ACCURACY_CHOICES,
    )
    name = models.CharField(_("Location"), blank=True)
    point = gis_models.PointField(_("Point"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    facility_name = models.CharField(_("Facility name"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]

    def __str__(self):
        return f"{self.nid} @ {self.dealversion}"


class Area(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="areas"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(choices=choices.AREA_TYPE_CHOICES)
    current = models.BooleanField(default=False)
    date = LooseDateField(_("Date"), blank=True, null=True)
    area = gis_models.MultiPolygonField()

    def __str__(self):
        return f"{self.location} >> {self.type}"

    # NOTE: Not in use, but would be nice to query features from backend directly
    def to_feature(self):
        return {
            "type": "Feature",
            "geometry": json.loads(self.area.geojson) if self.area else None,
            "properties": {
                "id": self.id,
                "type": self.type,
                "current": self.current,
                "date": self.date,
            },
        }

    @staticmethod
    def geometry_to_multipolygon(geom: GEOSGeometry | str | dict) -> MultiPolygon:
        if isinstance(geom, dict):
            geom = str(geom)
        if isinstance(geom, str):
            geom = GEOSGeometry(geom)
        if geom.hasz:
            wkt = wkt_w(dim=2).write(geom).decode()
            geom = GEOSGeometry(wkt, srid=4674)
        if isinstance(geom, MultiPolygon):
            return geom
        elif isinstance(geom, Polygon):
            return MultiPolygon([geom])

        raise ValidationError

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate_nid(Area)
        super().save(*args, **kwargs)

    class Meta:
        # unique_together = ["location", "type", "current"]
        ordering = ["id"]


class DealDataSource(BaseDataSource):
    dealversion = models.ForeignKey(
        DealVersion,
        on_delete=models.CASCADE,
        related_name="datasources",
    )

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


class DealWorkflowInfo(BaseWorkflowInfo):
    deal = models.ForeignKey(
        DealHull,
        on_delete=models.CASCADE,
        related_name="workflowinfos",
    )
    deal_version = models.ForeignKey(
        "DealVersion",
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/deal/{self.deal_id}/"


class Contract(models.Model):
    dealversion = models.ForeignKey(
        DealVersion,
        on_delete=models.CASCADE,
        related_name="contracts",
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    number = models.CharField(_("Contract number"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    expiration_date = LooseDateField(_("Expiration date"), blank=True, null=True)
    agreement_duration = models.IntegerField(
        _("Duration of the agreement"), blank=True, null=True
    )
    comment = models.TextField(_("Comment"), blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]
