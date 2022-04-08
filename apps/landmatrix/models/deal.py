import json
from typing import Optional

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Sum, F, Q
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.landmatrix.models import Investor
from apps.landmatrix.models.abstracts import (
    STATUS_CHOICES,
    DRAFT_STATUS_CHOICES,
    WorkflowInfo,
    STATUS,
    Version,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.fields import (
    LocationsField,
    ArrayField,
    ContractsField,
    DatasourcesField,
)
from apps.landmatrix.models.mixins import OldDealMixin


class DealQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=(2, 3))

    def public(self):
        return self.active().filter(is_public=True)

    def visible(self, user=None, subset="PUBLIC"):
        # TODO: welche user duerfen unfiltered bekommen?
        if not user or not user.is_authenticated:
            return self.public()

        if subset == "PUBLIC":
            return self.public()
        elif subset == "ACTIVE":
            return self.active()
        return self

    @staticmethod
    def _remove_filter(name, queryset):
        query = queryset.query
        query.where.children = [
            qx
            for qx in query.where.children
            if not hasattr(qx, "lhs")
            or (hasattr(qx, "lhs") and qx.lhs.target.name != name)
        ]

    def default_filtered(self, unset_filters: list = None):
        qs = (
            self.filter(deal_size__gte="200")
            .filter(
                current_negotiation_status__in=[
                    "ORAL_AGREEMENT",
                    "CONTRACT_SIGNED",
                ]
            )
            .exclude(nature_of_deal__contained_by=["PURE_CONTRACT_FARMING"])
            .filter(initiation_year__gte=2000)
            .exclude(
                current_intention_of_investment__overlap=[
                    "MINING",
                    "OIL_GAS_EXTRACTION",
                ]
            )
            .filter(transnational=True)
            .filter(forest_concession=False)
        )
        if unset_filters:
            [self._remove_filter(fltr, qs) for fltr in unset_filters]
        return qs

    def get_deal_country_rankings(self, country_id: int = None):
        rankings = (
            self.exclude(country=None)
            .values("country_id")
            .annotate(Sum("deal_size"))
            .order_by("-deal_size__sum")
        )
        if country_id:
            for i, rank in enumerate(rankings, start=1):
                if rank["country_id"] == country_id:
                    return i
            return
        return rankings

    def get_investor_country_rankings(self, country_id: int = None):
        rankings = (
            DealTopInvestors.objects.filter(deal__in=self)
            .values(country_id=F("investor__country__id"))
            .annotate(deal_size__sum=Sum("deal__deal_size"))
            .order_by("-deal_size__sum")
        )
        if country_id:
            for i, rank in enumerate(rankings, start=1):
                if rank["country_id"] == country_id:
                    return i
            return
        return rankings


class DealVersion(Version):
    object = models.ForeignKey(
        "Deal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="versions",
    )

    def to_dict(self):
        self.serialized_data["id"] = self.object_id
        return {
            "id": self.id,
            "object_id": self.object_id,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "deal": self.serialized_data,
        }


class Deal(models.Model, OldDealMixin):
    """Deal"""

    """ Locations """
    locations = LocationsField(_("Locations"), default=list)

    """ General info """
    # Land area
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="deals",
    )
    intended_size = models.DecimalField(
        _("Intended size (in ha)"),
        help_text=_("ha"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contract_size = models.JSONField(
        _("Size under contract (leased or purchased area, in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    production_size = models.JSONField(
        _("Size in operation (production, in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    land_area_comment = models.TextField(_("Comment on land area"), blank=True)

    # Intention of investment
    INTENTION_CHOICES = [
        ("BIOFUELS", _("Biofuels")),
        ("FOOD_CROPS", _("Food crops")),
        ("FODDER", _("Fodder")),
        ("LIVESTOCK", _("Livestock")),
        ("NON_FOOD_AGRICULTURE", _("Non-food agricultural commodities")),
        ("AGRICULTURE_UNSPECIFIED", _("Agriculture unspecified")),
        ("TIMBER_PLANTATION", _("Timber plantation")),
        ("FOREST_LOGGING", _("Forest logging / management")),
        ("CARBON", _("For carbon sequestration/REDD")),
        ("FORESTRY_UNSPECIFIED", _("Forestry unspecified")),
        ("MINING", _("Mining")),
        ("OIL_GAS_EXTRACTION", _("Oil / Gas extraction")),
        ("TOURISM", _("Tourism")),
        ("INDUSTRY", _("Industry")),
        ("CONVERSATION", _("Conservation")),
        ("LAND_SPECULATION", _("Land speculation")),
        ("RENEWABLE_ENERGY", _("Renewable energy")),
        ("OTHER", _("Other")),
    ]
    intention_of_investment = models.JSONField(
        _("Intention of investment"), choices=INTENTION_CHOICES, blank=True, null=True
    )
    intention_of_investment_comment = models.TextField(
        _("Comment on intention of investment"), blank=True
    )

    # Nature of the deal
    NATURE_OF_DEAL_CHOICES = (
        ("OUTRIGHT_PURCHASE", _("Outright purchase")),
        ("LEASE", _("Lease")),
        ("CONCESSION", _("Concession")),
        (
            "EXPLOITATION_PERMIT",
            _("Exploitation permit / license / concession (for mineral resources)"),
        ),
        ("PURE_CONTRACT_FARMING", _("Pure contract farming")),
        ("OTHER", _("Other")),
    )
    nature_of_deal = ArrayField(
        models.CharField(_("Nature of the deal"), max_length=100),
        verbose_name=_("Nature of the deal"),
        choices=NATURE_OF_DEAL_CHOICES,
        blank=True,
        null=True,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"), blank=True
    )

    # # Negotiation status
    NEGOTIATION_STATUS_CHOICES = [
        ("EXPRESSION_OF_INTEREST", "Expression of interest"),
        ("UNDER_NEGOTIATION", "Under negotiation"),
        ("MEMORANDUM_OF_UNDERSTANDING", "Memorandum of understanding"),
        ("ORAL_AGREEMENT", "Oral agreement"),
        ("CONTRACT_SIGNED", "Contract signed"),
        ("NEGOTIATIONS_FAILED", "Negotiations failed"),
        ("CONTRACT_CANCELED", "Contract canceled"),
        ("CONTRACT_EXPIRED", "Contract expired"),
        ("CHANGE_OF_OWNERSHIP", "Change of ownership"),
    ]
    negotiation_status = models.JSONField(
        _("Negotiation status"),
        choices=NEGOTIATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"), blank=True
    )

    # # Implementation status
    IMPLEMENTATION_STATUS_CHOICES = (
        ("PROJECT_NOT_STARTED", "Project not started"),
        ("STARTUP_PHASE", "Startup phase (no production)"),
        ("IN_OPERATION", "In operation (production)"),
        ("PROJECT_ABANDONED", "Project abandoned"),
    )
    implementation_status = models.JSONField(
        _("Implementation status"),
        choices=IMPLEMENTATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    implementation_status_comment = models.TextField(
        _("Comment on implementation status"), blank=True
    )

    # Purchase price
    purchase_price = models.DecimalField(
        _("Purchase price"), max_digits=18, decimal_places=2, blank=True, null=True
    )
    purchase_price_currency = models.ForeignKey(
        "Currency",
        verbose_name=_("Purchase price currency"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deal_purchase_price",
    )
    HA_AREA_CHOICES = (
        ("PER_HA", _("per ha")),
        ("PER_AREA", _("for specified area")),
    )
    purchase_price_type = models.CharField(
        _("Purchase price area type"),
        max_length=100,
        choices=HA_AREA_CHOICES,
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
        _("Comment on purchase price"), blank=True
    )

    # Leasing fees
    annual_leasing_fee = models.DecimalField(
        _("Annual leasing fee"), max_digits=18, decimal_places=2, blank=True, null=True
    )
    annual_leasing_fee_currency = models.ForeignKey(
        "Currency",
        verbose_name=_("Annual leasing fee currency"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deal_annual_leasing_fee",
    )
    annual_leasing_fee_type = models.CharField(
        _("Annual leasing fee area type"),
        max_length=100,
        choices=HA_AREA_CHOICES,
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
        _("Comment on leasing fee"), blank=True
    )

    # Contract farming
    # started implementing #113 . but not urgent, defering.
    # YES_IN_PLANNING_NO_CHOICES = (
    #     ("", _("Unknown")),
    #     ("YES", _("Yes")),
    #     ("IN_PLANNING", _("In Planning")),
    #     ("NO", _("No")),
    # )
    # contract_farming = models.CharField(choices=YES_IN_PLANNING_NO_CHOICES, default="")
    contract_farming = models.BooleanField(null=True)

    on_the_lease_state = models.BooleanField(_("On leased / purchased"), null=True)
    on_the_lease = models.JSONField(
        _("On leased area/farmers/households"),
        blank=True,
        null=True,
    )

    off_the_lease_state = models.BooleanField(
        _("Not on leased / purchased (out-grower)"), null=True
    )
    off_the_lease = models.JSONField(
        _("Not on leased area/farmers/households (out-grower)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )

    contract_farming_comment = models.TextField(
        _("Comment on contract farming"), blank=True
    )

    """ Contracts """
    contracts = ContractsField(_("Contracts"), default=list)

    """ Employment """
    total_jobs_created = models.BooleanField(_("Jobs created (total)"), null=True)
    total_jobs_planned = models.IntegerField(
        _("Planned number of jobs (total)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_planned_employees = models.IntegerField(
        _("Planned employees (total)"),
        help_text=_("employees"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (total)"),
        help_text=_("workers"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_current = models.JSONField(
        _("Current total number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        null=True,
    )
    total_jobs_created_comment = models.TextField(
        _("Comment on jobs created (total)"), blank=True
    )

    foreign_jobs_created = models.BooleanField(_("Jobs created (foreign)"), null=True)
    foreign_jobs_planned = models.IntegerField(
        _("Planned number of jobs (foreign)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_planned_employees = models.IntegerField(
        _("Planned employees (foreign)"),
        help_text=_("employees"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (foreign)"),
        help_text=_("workers"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_current = models.JSONField(
        _("Current foreign number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        null=True,
    )
    foreign_jobs_created_comment = models.TextField(
        _("Comment on jobs created (foreign)"), blank=True
    )

    domestic_jobs_created = models.BooleanField(_("Jobs created (domestic)"), null=True)
    domestic_jobs_planned = models.IntegerField(
        _("Planned number of jobs (domestic)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_planned_employees = models.IntegerField(
        _("Planned employees (domestic)"),
        help_text=_("employees"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (domestic)"),
        help_text=_("workers"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_current = models.JSONField(
        _("Current domestic number of jobs/employees/ daily/seasonal workers"),
        blank=True,
        null=True,
    )
    domestic_jobs_created_comment = models.TextField(
        _("Comment on jobs created (domestic)"), blank=True
    )

    """ Investor info """
    operating_company = models.ForeignKey(
        Investor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="deals",
    )
    ACTOR_MAP = (
        (
            "GOVERNMENT_OR_STATE_INSTITUTIONS",
            _(
                "Government / state institutions (government, ministries, departments, agencies etc.)"
            ),
        ),
        (
            "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
            _("Traditional land-owners / communities"),
        ),
        (
            "TRADITIONAL_LOCAL_AUTHORITY",
            _("Traditional local authority (e.g. Chiefdom council / Chiefs)"),
        ),
        ("BROKER", _("Broker")),
        ("INTERMEDIARY", _("Intermediary")),
        ("OTHER", _("Other (please specify)")),
    )
    involved_actors = models.JSONField(
        _("Actors involved in the negotiation / admission process"),
        choices=ACTOR_MAP,
        blank=True,
        null=True,
    )
    project_name = models.CharField(
        _("Name of investment project"), max_length=255, blank=True
    )
    investment_chain_comment = models.TextField(
        _("Comment on investment chain"), blank=True
    )

    """ Data sources """
    datasources = DatasourcesField(_("Data sources"), default=list)

    """ Local communities / indigenous peoples """
    name_of_community = ArrayField(
        models.CharField(_("Name of community"), max_length=255), blank=True, null=True
    )
    name_of_indigenous_people = ArrayField(
        models.CharField(_("Name of indigenous people"), max_length=255),
        blank=True,
        null=True,
    )
    people_affected_comment = models.TextField(
        _("Comment on communities / indigenous peoples affected"), blank=True
    )

    RECOGNITION_STATUS_CHOICES = (
        (
            "INDIGENOUS_RIGHTS_RECOGNIZED",
            _(
                "Indigenous Peoples traditional or customary rights recognized by government"
            ),
        ),
        (
            "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
            _(
                "Indigenous Peoples traditional or customary rights not recognized by government"
            ),
        ),
        (
            "COMMUNITY_RIGHTS_RECOGNIZED",
            _("Community traditional or customary rights recognized by government"),
        ),
        (
            "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
            _("Community traditional or customary rights not recognized by government"),
        ),
    )
    recognition_status = ArrayField(
        models.CharField(
            _("Recognition status of community land tenure"),
            max_length=100,
        ),
        choices=RECOGNITION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognition status of community land tenure"), blank=True
    )
    COMMUNITY_CONSULTATION_CHOICES = (
        ("NOT_CONSULTED", _("Not consulted")),
        ("LIMITED_CONSULTATION", _("Limited consultation")),
        ("FPIC", _("Free, Prior and Informed Consent (FPIC)")),
        ("OTHER", _("Other")),
    )
    community_consultation = models.CharField(
        _("Community consultation"),
        max_length=100,
        choices=COMMUNITY_CONSULTATION_CHOICES,
        blank=True,
        null=True,
    )
    community_consultation_comment = models.TextField(
        _("Comment on consultation of local community"), blank=True
    )

    COMMUNITY_REACTION_CHOICES = (
        ("CONSENT", _("Consent")),
        ("MIXED_REACTION", _("Mixed reaction")),
        ("REJECTION", _("Rejection")),
    )
    community_reaction = models.CharField(
        _("Community reaction"),
        max_length=100,
        choices=COMMUNITY_REACTION_CHOICES,
        blank=True,
        null=True,
    )
    community_reaction_comment = models.TextField(
        _("Comment on community reaction"), blank=True
    )

    land_conflicts = models.BooleanField(_("Presence of land conflicts"), null=True)
    land_conflicts_comment = models.TextField(
        _("Comment on presence of land conflicts"), blank=True
    )

    displacement_of_people = models.BooleanField(_("Displacement of people"), null=True)
    displaced_people = models.IntegerField(
        _("Number of people actually displaced"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displaced_households = models.IntegerField(
        _("Number of households actually displaced"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displaced_people_from_community_land = models.IntegerField(
        _("Number of people displaced out of their community land"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displaced_people_within_community_land = models.IntegerField(
        _("Number of people displaced staying on community land"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displaced_households_from_fields = models.IntegerField(
        _('Number of households displaced "only" from their agricultural fields'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displaced_people_on_completion = models.IntegerField(
        _("Number of people facing displacement once project is fully implemented"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    displacement_of_people_comment = models.TextField(
        _("Comment on displacement of people"), blank=True
    )

    NEGATIVE_IMPACTS_CHOICES = (
        ("ENVIRONMENTAL_DEGRADATION", _("Environmental degradation")),
        ("SOCIO_ECONOMIC", _("Socio-economic")),
        ("CULTURAL_LOSS", _("Cultural loss")),
        ("EVICTION", _("Eviction")),
        ("DISPLACEMENT", _("Displacement")),
        ("VIOLENCE", _("Violence")),
        ("OTHER", _("Other")),
    )
    negative_impacts = ArrayField(
        models.CharField(_("Negative impacts for local communities"), max_length=100),
        choices=NEGATIVE_IMPACTS_CHOICES,
        blank=True,
        null=True,
    )
    negative_impacts_comment = models.TextField(
        _("Comment on negative impacts for local communities"), blank=True
    )

    promised_compensation = models.TextField(
        _("Promised compensation (e.g. for damages or resettlements)"), blank=True
    )
    received_compensation = models.TextField(
        _("Received compensation (e.g. for damages or resettlements)"), blank=True
    )

    BENEFITS_CHOICES = (
        ("HEALTH", _("Health")),
        ("EDUCATION", _("Education")),
        (
            "PRODUCTIVE_INFRASTRUCTURE",
            _("Productive infrastructure (e.g. irrigation, tractors, machinery...)"),
        ),
        ("ROADS", _("Roads")),
        ("CAPACITY_BUILDING", _("Capacity building")),
        ("FINANCIAL_SUPPORT", _("Financial support")),
        ("COMMUNITY_SHARES", _("Community shares in the investment project")),
        ("OTHER", _("Other")),
    )
    promised_benefits = ArrayField(
        models.CharField(_("Promised benefits for local communities"), max_length=100),
        choices=BENEFITS_CHOICES,
        blank=True,
        null=True,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    materialized_benefits = ArrayField(
        models.CharField(
            _("Materialized benefits for local communities"),
            max_length=100,
        ),
        choices=BENEFITS_CHOICES,
        blank=True,
        null=True,
    )
    materialized_benefits_comment = models.TextField(
        _("Comment on materialized benefits for local communities"), blank=True
    )

    presence_of_organizations = models.TextField(
        _(
            "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"
        ),
        blank=True,
    )

    """ Former use """
    FORMER_LAND_OWNER_CHOICES = (
        ("STATE", _("State")),
        ("PRIVATE_SMALLHOLDERS", _("Private (smallholders)")),
        ("PRIVATE_LARGE_SCALE", _("Private (large-scale farm)")),
        ("COMMUNITY", _("Community")),
        ("INDIGENOUS_PEOPLE", _("Indigenous people")),
        ("OTHER", _("Other")),
    )
    former_land_owner = ArrayField(
        models.CharField(max_length=100),
        verbose_name=_("Former land owner"),
        choices=FORMER_LAND_OWNER_CHOICES,
        blank=True,
        null=True,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )

    FORMER_LAND_USE_CHOICES = (
        ("COMMERCIAL_AGRICULTURE", _("Commercial (large-scale) agriculture")),
        ("SMALLHOLDER_AGRICULTURE", _("Smallholder agriculture")),
        ("SHIFTING_CULTIVATION", _("Shifting cultivation")),
        ("PASTORALISM", _("Pastoralism")),
        ("HUNTING_GATHERING", _("Hunting/Gathering")),
        ("FORESTRY", _("Forestry")),
        ("CONSERVATION", _("Conservation")),
        ("OTHER", _("Other")),
    )

    former_land_use = ArrayField(
        models.CharField(max_length=100),
        verbose_name=_("Former land use"),
        choices=FORMER_LAND_USE_CHOICES,
        blank=True,
        null=True,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )

    FORMER_LAND_COVER_CHOICES = (
        ("CROPLAND", _("Cropland")),
        ("FOREST_LAND", _("Forest land")),
        ("PASTURE", _("Pasture")),
        ("RANGELAND", _("Shrub land/Grassland (Rangeland)")),
        ("MARGINAL_LAND", _("Marginal land")),
        ("WETLAND", _("Wetland")),
        (
            "OTHER_LAND",
            _("Other land (e.g. developed land – specify in comment field)"),
        ),
    )

    former_land_cover = ArrayField(
        models.CharField(max_length=100),
        verbose_name=_("Former land cover"),
        choices=FORMER_LAND_COVER_CHOICES,
        blank=True,
        null=True,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"), blank=True
    )

    """ Produce info """
    crops = models.JSONField(_("Crops area/yield/export"), blank=True, null=True)
    crops_comment = models.TextField(_("Comment on crops"), blank=True)

    animals = models.JSONField(_("Livestock area/yield/export"), blank=True, null=True)
    animals_comment = models.TextField(_("Comment on livestock"), blank=True)

    mineral_resources = models.JSONField(
        _("Mineral resources area/yield/export"), blank=True, null=True
    )
    mineral_resources_comment = models.TextField(
        _("Comment on mineral resources"), blank=True
    )

    contract_farming_crops = models.JSONField(
        _("Contract farming crops"), help_text=_("ha"), blank=True, null=True
    )
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"), blank=True
    )
    contract_farming_animals = models.JSONField(
        _("Contract farming livestock"), help_text=_("ha"), blank=True, null=True
    )
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"), blank=True
    )

    has_domestic_use = models.BooleanField(_("Has domestic use"), null=True)
    domestic_use = models.FloatField(
        _("Domestic use"),
        help_text="%",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    has_export = models.BooleanField(_("Has export"), null=True)

    export = models.FloatField(
        _("Export"),
        help_text="%",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    export_country1 = models.ForeignKey(
        Country,
        verbose_name=_("Country 1"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country1_ratio = models.FloatField(
        _("Country 1 ratio"),
        help_text="%",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country2 = models.ForeignKey(
        Country,
        verbose_name=_("Country 2"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country2_ratio = models.FloatField(
        _("Country 2 ratio"),
        help_text="%",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country3 = models.ForeignKey(
        Country,
        verbose_name=_("Country 3"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    export_country3_ratio = models.FloatField(
        _("Country 3 ratio"),
        help_text="%",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    use_of_produce_comment = models.TextField(
        verbose_name=_("Comment on use of produce"), blank=True
    )

    in_country_processing = models.BooleanField(
        _("In country processing of produce"), null=True
    )
    in_country_processing_comment = models.TextField(
        _("Comment on in country processing of produce"), blank=True
    )
    in_country_processing_facilities = models.TextField(
        _(
            "Processing facilities / production infrastructure of the project"
            " (e.g. oil mill, ethanol distillery, biomass power plant etc.)"
        ),
        blank=True,
    )
    in_country_end_products = models.TextField(
        _("In-country end products of the project"), blank=True
    )

    """Water"""
    water_extraction_envisaged = models.BooleanField(
        _("Water extraction envisaged"), null=True
    )
    water_extraction_envisaged_comment = models.TextField(
        _("Comment on water extraction envisaged"), blank=True
    )

    WATER_SOURCE_CHOICES = (
        ("GROUNDWATER", "Groundwater"),
        ("SURFACE_WATER", "Surface water"),
        ("RIVER", "River"),
        ("LAKE", "Lake"),
    )
    source_of_water_extraction = ArrayField(
        models.CharField(max_length=100),
        verbose_name=_("Source of water extraction"),
        choices=WATER_SOURCE_CHOICES,
        blank=True,
        null=True,
    )
    source_of_water_extraction_comment = models.TextField(
        _("Comment on source of water extraction"), blank=True
    )
    how_much_do_investors_pay_comment = models.TextField(
        _("Comment on how much do investors pay for water"), blank=True
    )

    water_extraction_amount = models.IntegerField(
        _("Water extraction amount"), help_text=_("m3/year"), blank=True, null=True
    )
    water_extraction_amount_comment = models.TextField(
        _("Comment on how much water is extracted"), blank=True
    )
    use_of_irrigation_infrastructure = models.BooleanField(
        _("Use of irrigation infrastructure"), null=True
    )
    use_of_irrigation_infrastructure_comment = models.TextField(
        _("Comment on use of irrigation infrastructure"), blank=True
    )
    water_footprint = models.TextField(
        _("Water footprint of the investment project"), blank=True
    )

    """ Gender-related info """
    gender_related_information = models.TextField(
        _("Comment on gender-related info"), blank=True
    )

    """ Overall comment """
    overall_comment = models.TextField(_("Overall comment"), blank=True)

    """ Meta Info """
    fully_updated = models.BooleanField(default=False)
    confidential = models.BooleanField(default=False)
    CONFIDENTIAL_REASON_CHOICES = (
        ("TEMPORARY_REMOVAL", _("Temporary removal from PI after criticism")),
        ("RESEARCH_IN_PROGRESS", _("Research in progress")),
        ("LAND_OBSERVATORY_IMPORT", _("Land Observatory Import")),
    )
    confidential_reason = models.CharField(
        max_length=100, choices=CONFIDENTIAL_REASON_CHOICES, null=True, blank=True
    )
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True, null=True
    )

    """ # CALCULATED FIELDS # """
    is_public = models.BooleanField(default=False)
    has_known_investor = models.BooleanField(default=False)
    NOT_PUBLIC_REASON_CHOICES = (
        ("CONFIDENTIAL", "Confidential flag"),
        ("NO_COUNTRY", "No country"),
        ("HIGH_INCOME_COUNTRY", "High-income country"),
        ("NO_DATASOURCES", "No datasources"),
        ("NO_OPERATING_COMPANY", "No operating company"),
        ("NO_KNOWN_INVESTOR", "No known investor"),
    )
    not_public_reason = models.CharField(
        max_length=100, blank=True, choices=NOT_PUBLIC_REASON_CHOICES
    )
    parent_companies = models.ManyToManyField(
        Investor, verbose_name=_("Parent companies"), related_name="child_deals"
    )
    top_investors = models.ManyToManyField(
        Investor, verbose_name=_("Top parent companies"), related_name="+"
    )
    current_contract_size = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_production_size = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_intention_of_investment = ArrayField(
        models.CharField(max_length=100),
        choices=INTENTION_CHOICES,
        blank=True,
        null=True,
    )
    current_negotiation_status = models.CharField(
        choices=NEGOTIATION_STATUS_CHOICES, max_length=100, blank=True, null=True
    )
    current_implementation_status = models.CharField(
        choices=IMPLEMENTATION_STATUS_CHOICES, max_length=100, blank=True, null=True
    )
    current_crops = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    current_animals = ArrayField(
        models.CharField(max_length=100), blank=True, null=True
    )
    current_mineral_resources = ArrayField(
        models.CharField(max_length=100), blank=True, null=True
    )

    deal_size = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    initiation_year = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1970)]
    )
    forest_concession = models.BooleanField(default=False)
    transnational = models.BooleanField(null=True)
    geojson = models.JSONField(blank=True, null=True)

    """ # Status """
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    current_draft = models.ForeignKey(
        DealVersion, null=True, blank=True, on_delete=models.SET_NULL
    )

    """ # Timestamps """
    created_at = models.DateTimeField(_("Created"), default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Last update"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    fully_updated_at = models.DateTimeField(
        _("Last full update"), blank=True, null=True
    )

    objects = DealQuerySet.as_manager()

    def __str__(self):
        if self.country:
            return f"#{self.id} in {self.country}"
        return f"#{self.id}"

    def recalculate_fields(self, independent=True, dependent=True):
        if independent:
            self.current_contract_size = self._get_current("contract_size", "area")
            self.current_production_size = self._get_current("production_size", "area")
            self.current_intention_of_investment = self._get_current(
                "intention_of_investment", "choices"
            )
            self.current_negotiation_status = self._get_current(
                "negotiation_status", "choice"
            )
            self.current_implementation_status = self._get_current(
                "implementation_status", "choice"
            )
            self.current_crops = self._get_current("crops", "choices")
            self.current_animals = self._get_current("animals", "choices")
            self.current_mineral_resources = self._get_current(
                "mineral_resources", "choices"
            )

            # these only depend on the _get_current calls right above.
            self.deal_size = self._calculate_deal_size()
            self.initiation_year = self._calculate_initiation_year()
            self.forest_concession = self._calculate_forest_concession()
        if dependent:
            # With the help of signals these fields are recalculated on changes to:
            # Investor and InvestorVentureInvolvement
            self.has_known_investor = not self._has_no_known_investor()
            self.not_public_reason = self._calculate_public_state()
            self.is_public = self.not_public_reason == ""
            # this might error because it's m2m and we need the
            # Deal to have an ID first before we can save the investors. 🙄
            self._calculate_parent_companies()
            self.transnational = self._calculate_transnational()
            self.geojson = self._combine_geojson()

    @transaction.atomic
    def save(
        self, recalculate_independent=True, recalculate_dependent=True, *args, **kwargs
    ):
        self.recalculate_fields(recalculate_independent, recalculate_dependent)
        super().save(*args, **kwargs)

    def update_from_dict(self, d: dict):
        for key, value in d.items():
            if key in [
                "id",
                "created_at",
                "modified_at",
                "fully_updated",
                "fully_updated_at",
                "is_public",
                "has_known_investor",
                "versions",
                "comments",
                "status",
                "draft_status",
                "workflowinfos",
                "__typename",
            ]:
                continue  # ignore these fields
            elif key in [
                x.name
                for x in self._meta.fields
                if x.__class__.__name__ == "ForeignKey"
            ]:
                self.__setattr__(f"{key}_id", value["id"] if value else None)
            elif key == "point":
                self.point = Point(value["lng"], value["lat"])
            elif key in ["locations", "datasources", "contracts"]:
                new_value = [
                    val
                    for val in value
                    if any([v for k, v in val.items() if k != "id"])
                ]
                self.__setattr__(key, new_value)

            else:
                self.__setattr__(key, value)

    def serialize_for_version(self) -> dict:
        serialized_json = serializers.serialize("json", (self,))
        return json.loads(serialized_json)[0]["fields"]

    @staticmethod
    def deserialize_from_version(version: DealVersion) -> "Deal":
        daty = {
            "pk": version.object_id,
            "model": "landmatrix.deal",
            "fields": version.serialized_data,
        }
        obj = list(serializers.deserialize("json", json.dumps([daty])))[0].object
        obj.save()
        return obj

    def _get_current(self, attribute, field):
        attributes: list = self.__getattribute__(attribute)
        if not attributes:
            return None
        # prioritize "current" checkbox if present
        current = [x for x in attributes if x.get("current")]
        if current:
            return current[0].get(field)
        else:
            print(self)
            print(attribute)
            print(attributes)
            raise Exception("We should always have a current, now.")

    def _calculate_deal_size(self):
        negotiation_status = self.current_negotiation_status
        if not negotiation_status:
            return 0

        intended_size = self.intended_size or 0.0
        contract_size = self.current_contract_size or 0.0
        production_size = self.current_production_size or 0.0

        # 1) IF Negotiation status IS Intended
        if negotiation_status in (
            "EXPRESSION_OF_INTEREST",
            "UNDER_NEGOTIATION",
            "MEMORANDUM_OF_UNDERSTANDING",
        ):
            # USE Intended size OR Contract size OR Production size (in the given order)
            value = intended_size or contract_size or production_size
        # 2) IF Negotiation status IS Concluded
        elif negotiation_status in ("ORAL_AGREEMENT", "CONTRACT_SIGNED"):
            # USE Contract size or Production size (in the given order)
            value = contract_size or production_size
        # 3) IF Negotiation status IS Failed (Negotiations failed)
        elif negotiation_status == "NEGOTIATIONS_FAILED":
            # USE Intended size OR Contract size OR Production size (in the given order)
            value = intended_size or contract_size or production_size
        # 4) IF Negotiation status IS Failed (Contract canceled)
        elif negotiation_status == "CONTRACT_CANCELED":
            # USE Contract size OR Production size (in the given order)
            value = contract_size or production_size
        # 5) IF Negotiation status IS Contract expired
        elif negotiation_status == "CONTRACT_EXPIRED":
            # USE Contract size OR Production size (in the given order)
            value = contract_size or production_size
        # 6) IF Negotiation status IS Change of ownership
        elif negotiation_status == "CHANGE_OF_OWNERSHIP":
            # USE Contract size OR Production size (in the given order)
            value = contract_size or production_size
        else:
            value = 0.0
        return value

    def _calculate_initiation_year(self):
        valid_negotation_status = (
            [
                int(x["date"][:4])
                for x in self.negotiation_status
                if x.get("date")
                and x["choice"]
                in (
                    "UNDER_NEGOTIATION",
                    "ORAL_AGREEMENT",
                    "CONTRACT_SIGNED",
                    "NEGOTIATIONS_FAILED",
                    "CONTRACT_CANCELED",
                )
            ]
            if self.negotiation_status
            else []
        )
        valid_implementation_status = (
            [
                int(x["date"][:4])
                for x in self.implementation_status
                if x.get("date")
                and x["choice"]
                in (
                    "STARTUP_PHASE",
                    "IN_OPERATION",
                    "PROJECT_ABANDONED",
                )
            ]
            if self.implementation_status
            else []
        )
        dates = valid_implementation_status + valid_negotation_status
        return min(dates) if dates else None

    def _calculate_forest_concession(self) -> bool:
        return bool(
            self.nature_of_deal
            and "CONCESSION" in self.nature_of_deal
            and self.current_intention_of_investment
            and "FOREST_LOGGING" in self.current_intention_of_investment
        )

    def _calculate_transnational(self) -> Optional[bool]:
        if not self.country_id:
            # unknown if we have no target country
            return None

        # by definition True, if no operating company exists (or it is deleted)
        if not self.operating_company_id:
            return True
        oc = Investor.objects.get(id=self.operating_company_id)
        if oc.status == STATUS["DELETED"]:
            return True

        investors_countries = self.parent_companies.exclude(
            country_id=None
        ).values_list("country_id", flat=True)

        if not len(investors_countries):
            # treat deals without investors as transnational
            # treat deals without investor countries as transnational
            return True
        # `True` if we have investors in other countries else `False`
        return bool(set(investors_countries) - {self.country_id})

    def _combine_geojson(self):
        features = []
        for i, loc in enumerate(self.locations or [], 1):  # type: dict
            if loc.get("point"):
                point = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [loc["point"]["lng"], loc["point"]["lat"]],
                    },
                    "properties": {
                        "id": i,
                        "name": loc.get("name"),
                        "type": "point",
                        "spatial_accuracy": loc.get("level_of_accuracy"),
                    },
                }
                features += [point]
            areas = loc.get("areas")
            if areas:
                feats = areas["features"]
                for feat in feats:
                    feat["properties"]["name"] = loc.get("name")
                    feat["properties"]["id"] = i
                    if (
                        feat["geometry"]["type"] == "MultiPolygon"
                        and len(feat["geometry"]["coordinates"]) == 1
                    ):
                        feat["geometry"]["type"] = "Polygon"
                        feat["geometry"]["coordinates"] = feat["geometry"][
                            "coordinates"
                        ][0]
                    features += [feat]
        if not features:
            return None
        return {"type": "FeatureCollection", "features": features}

    def _calculate_parent_companies(self) -> None:
        if self.operating_company_id:
            oc = Investor.objects.filter(
                id=self.operating_company_id,
                status__in=[STATUS["LIVE"], STATUS["UPDATED"]],
            ).first()
            if oc:
                parent_companies = oc.get_parent_companies()
                self.parent_companies.set(parent_companies)
                top_inv = [x for x in parent_companies if x.is_top_investor]
                self.top_investors.set(top_inv)
                return
        if self.id:
            self.parent_companies.set([])
            self.top_investors.set([])

    def _calculate_public_state(self) -> str:
        """
        :return: A string with a value if not public, or empty if public
        """
        if self.confidential:
            # 1. Flag "confidential"
            return "CONFIDENTIAL"
        if not self.country_id:
            # No Country
            return "NO_COUNTRY"
        # the following Country query is intentional. it has to do with country not
        # neccessarily being set, when country_id is set.
        if Country.objects.get(id=self.country_id).high_income:
            # High Income Country
            return "HIGH_INCOME_COUNTRY"
        if not self.datasources:
            # No DataSource
            return "NO_DATASOURCES"
        if not self.operating_company_id:
            # 3. No operating company
            return "NO_OPERATING_COMPANY"
        if not self.has_known_investor:
            # 4. Unknown operating company AND no known operating company parents
            return "NO_KNOWN_INVESTOR"
        return ""

    def _has_no_known_investor(self) -> bool:
        if not self.operating_company_id:
            return True
        oc = Investor.objects.get(id=self.operating_company_id)
        # if the Operating Company is known, we have a known investor and exit.
        if not oc.is_actually_unknown:
            return False
        # only if no known Investor exists, we return True
        return not oc.investors.filter(investor__is_actually_unknown=False).exists()


class DealWorkflowInfo(WorkflowInfo):
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    deal_version = models.ForeignKey(
        DealVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"deal": self.deal, "deal_version": self.deal_version})
        return d


class DealParentCompanies(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="+")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="+")

    class Meta:
        managed = False
        db_table = "landmatrix_deal_parent_companies"

    def __str__(self):
        return f"#{self.deal_id} - {self.investor.name}"


class DealTopInvestors(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="+")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="+")

    class Meta:
        managed = False
        db_table = "landmatrix_deal_top_investors"

    def __str__(self):
        return f"#{self.deal_id} - {self.investor.name}"
