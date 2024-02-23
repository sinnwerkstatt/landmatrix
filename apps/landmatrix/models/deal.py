import json

from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F, Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from . import choices
from .abstracts import (
    DRAFT_STATUS_CHOICES,
    STATUS,
    STATUS_CHOICES,
    Version,
    WorkflowInfo,
)
from .country import Country
from .currency import Currency
from .fields import ArrayField
from .oldfields import ContractsField, DatasourcesField, LocationsField
from .investor import Investor


class DealQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=(2, 3))

    def public(self):
        return self.active().filter(is_public=True)

    def visible(self, user=None, subset="PUBLIC"):
        if not user or not user.is_authenticated:
            return self.public()

        if subset == "PUBLIC":
            return self.public()
        elif subset == "ACTIVE":
            return self.active()
        return self

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
        "DealOld",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="versions",
    )


class AbstractDealBase(models.Model):
    """Deal Payload"""

    """ Locations """
    locations = LocationsField(_("Locations"), default=list, blank=True)

    """ General info """
    # Land area
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="oldmodel_deals",
    )
    intended_size = models.DecimalField(
        _("Intended size"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contract_size = models.JSONField(blank=True, null=True)
    production_size = models.JSONField(blank=True, null=True)
    land_area_comment = models.TextField(_("Comment on land area"), blank=True)

    # Intention of investment
    intention_of_investment = models.JSONField(blank=True, null=True)
    intention_of_investment_comment = models.TextField(
        _("Comment on intention of investment"), blank=True
    )

    # Nature of the deal
    nature_of_deal = ArrayField(
        models.CharField(choices=choices.NATURE_OF_DEAL_CHOICES),
        verbose_name=_("Nature of the deal"),
        blank=True,
        null=True,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"), blank=True
    )

    # # Negotiation status
    negotiation_status = models.JSONField(blank=True, null=True)
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"), blank=True
    )

    # # Implementation status
    implementation_status = models.JSONField(blank=True, null=True)
    implementation_status_comment = models.TextField(
        _("Comment on implementation status"), blank=True
    )

    # Purchase price
    purchase_price = models.DecimalField(
        _("Purchase price"), max_digits=18, decimal_places=2, blank=True, null=True
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
        _("Comment on purchase price"), blank=True
    )

    # Leasing fees
    annual_leasing_fee = models.DecimalField(
        _("Annual leasing fee"), max_digits=18, decimal_places=2, blank=True, null=True
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
    # models.CharField(choices=YES_IN_PLANNING_NO_CHOICES, default="")
    contract_farming = models.BooleanField(null=True)

    on_the_lease_state = models.BooleanField(_("On leased / purchased"), null=True)
    on_the_lease = models.JSONField(blank=True, null=True)

    off_the_lease_state = models.BooleanField(
        _("Not on leased / purchased (out-grower)"), null=True
    )
    off_the_lease = models.JSONField(blank=True, null=True)

    contract_farming_comment = models.TextField(
        _("Comment on contract farming"), blank=True
    )

    """ Contracts """
    contracts = ContractsField(_("Contracts"), default=list, blank=True)

    """ Employment """
    total_jobs_created = models.BooleanField(_("Jobs created (total)"), null=True)
    total_jobs_planned = models.IntegerField(
        _("Planned number of jobs (total)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_planned_employees = models.IntegerField(
        _("Planned employees (total)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (total)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    total_jobs_current = models.JSONField(blank=True, null=True)
    total_jobs_created_comment = models.TextField(
        _("Comment on jobs created (total)"), blank=True
    )

    foreign_jobs_created = models.BooleanField(_("Jobs created (foreign)"), null=True)
    foreign_jobs_planned = models.IntegerField(
        _("Planned number of jobs (foreign)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_planned_employees = models.IntegerField(
        _("Planned employees (foreign)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (foreign)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    foreign_jobs_current = models.JSONField(blank=True, null=True)
    foreign_jobs_created_comment = models.TextField(
        _("Comment on jobs created (foreign)"), blank=True
    )

    domestic_jobs_created = models.BooleanField(_("Jobs created (domestic)"), null=True)
    domestic_jobs_planned = models.IntegerField(
        _("Planned number of jobs (domestic)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_planned_employees = models.IntegerField(
        _("Planned employees (domestic)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (domestic)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    domestic_jobs_current = models.JSONField(blank=True, null=True)
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
    involved_actors = models.JSONField(blank=True, null=True)
    project_name = models.CharField(_("Name of investment project"), blank=True)
    investment_chain_comment = models.TextField(
        _("Comment on investment chain"), blank=True
    )

    """ Data sources """
    datasources = DatasourcesField(_("Data sources"), default=list, blank=True)

    """ Local communities / indigenous peoples """
    name_of_community = ArrayField(
        models.CharField(blank=True),
        verbose_name=_("Name of community"),
        blank=True,
        null=True,
    )
    name_of_indigenous_people = ArrayField(
        models.CharField(blank=True),
        verbose_name=_("Name of indigenous people"),
        blank=True,
        null=True,
    )
    people_affected_comment = models.TextField(
        _("Comment on communities / indigenous peoples affected"), blank=True
    )

    recognition_status = ArrayField(
        models.CharField(choices=choices.RECOGNITION_STATUS_CHOICES),
        verbose_name=_("Recognition status of community land tenure"),
        blank=True,
        null=True,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognition status of community land tenure"), blank=True
    )
    community_consultation = models.CharField(
        _("Community consultation"),
        choices=choices.COMMUNITY_CONSULTATION_CHOICES,
        blank=True,
        null=True,
    )
    community_consultation_comment = models.TextField(
        _("Comment on consultation of local community"), blank=True
    )

    community_reaction = models.CharField(
        _("Community reaction"),
        choices=choices.COMMUNITY_REACTION_CHOICES,
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

    negative_impacts = ArrayField(
        models.CharField(choices=choices.NEGATIVE_IMPACTS_CHOICES),
        verbose_name=_("Negative impacts for local communities"),
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

    promised_benefits = ArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Promised benefits for local communities"),
        blank=True,
        null=True,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    materialized_benefits = ArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Materialized benefits for local communities"),
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

    former_land_owner = ArrayField(
        models.CharField(choices=choices.FORMER_LAND_OWNER_CHOICES),
        verbose_name=_("Former land owner"),
        blank=True,
        null=True,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )

    former_land_use = ArrayField(
        models.CharField(choices=choices.FORMER_LAND_USE_CHOICES),
        verbose_name=_("Former land use"),
        blank=True,
        null=True,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )

    former_land_cover = ArrayField(
        models.CharField(choices=choices.FORMER_LAND_COVER_CHOICES),
        verbose_name=_("Former land cover"),
        blank=True,
        null=True,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"), blank=True
    )

    """ Produce info """
    crops = models.JSONField(blank=True, null=True)
    crops_comment = models.TextField(_("Comment on crops"), blank=True)

    animals = models.JSONField(blank=True, null=True)
    animals_comment = models.TextField(_("Comment on livestock"), blank=True)

    mineral_resources = models.JSONField(blank=True, null=True)
    mineral_resources_comment = models.TextField(
        _("Comment on mineral resources"), blank=True
    )

    contract_farming_crops = models.JSONField(blank=True, null=True)
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"), blank=True
    )
    contract_farming_animals = models.JSONField(blank=True, null=True)
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"), blank=True
    )

    electricity_generation = models.JSONField(blank=True, null=True)
    electricity_generation_comment = models.TextField(
        _("Comment on electricity generation"), blank=True
    )
    carbon_sequestration = models.JSONField(blank=True, null=True)
    carbon_sequestration_comment = models.TextField(
        _("Comment on carbon sequestration"), blank=True
    )

    has_domestic_use = models.BooleanField(_("Has domestic use"), null=True)
    domestic_use = models.FloatField(
        _("Domestic use"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    has_export = models.BooleanField(_("Has export"), null=True)

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

    source_of_water_extraction = ArrayField(
        models.CharField(choices=choices.WATER_SOURCE_CHOICES),
        verbose_name=_("Source of water extraction"),
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
        _("Water extraction amount"), blank=True, null=True
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

    class Meta:
        abstract = True


class DealOld(AbstractDealBase):
    """Meta Info"""

    fully_updated = models.BooleanField(default=False)
    confidential = models.BooleanField(default=False)
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True, null=True
    )

    """ # CALCULATED FIELDS # """
    is_public = models.BooleanField(default=False)
    has_known_investor = models.BooleanField(default=False)
    not_public_reason = models.CharField(
        blank=True, choices=choices.NOT_PUBLIC_REASON_CHOICES
    )
    # NOTE: Next two fields should have used through keyword.
    # Can be queried via DealParentCompanies view model.
    parent_companies = models.ManyToManyField(
        Investor,
        verbose_name=_("Parent companies"),
        related_name="child_deals",
    )
    # Can be queried via DealTopInvestors view model.
    top_investors = models.ManyToManyField(
        Investor,
        verbose_name=_("Top parent companies"),
        related_name="+",
    )
    current_contract_size = models.DecimalField(
        verbose_name=_("Current contract size"),
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
        models.CharField(choices=choices.INTENTION_OF_INVESTMENT_CHOICES),
        blank=True,
        null=True,
    )
    current_negotiation_status = models.CharField(
        choices=choices.NEGOTIATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    current_implementation_status = models.CharField(
        choices=choices.IMPLEMENTATION_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    current_crops = ArrayField(models.CharField(), blank=True, null=True)
    current_animals = ArrayField(models.CharField(), blank=True, null=True)
    current_mineral_resources = ArrayField(models.CharField(), blank=True, null=True)
    current_electricity_generation = ArrayField(
        models.CharField(), blank=True, null=True
    )
    current_carbon_sequestration = ArrayField(models.CharField(), blank=True, null=True)

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
    # geojson is a single FeatureCollection object or None (but never a list!)
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
    created_at = models.DateTimeField(_("Created"), default=timezone.now, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Last update"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
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


class DealWorkflowInfoOld(WorkflowInfo):
    deal = models.ForeignKey(
        DealOld, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    deal_version = models.ForeignKey(
        DealVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )


class DealOldParentCompanies(models.Model):
    """A view on deal.parent_companies M2M relation table."""

    deal = models.ForeignKey(DealOld, on_delete=models.CASCADE, related_name="+")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="+")

    class Meta:
        managed = False
        db_table = "landmatrix_deal_parent_companies"

    def __str__(self):
        return f"#{self.deal_id} - {self.investor.name}"


class DealTopInvestors(models.Model):
    """A view on deal.top_investors M2M relation table."""

    deal = models.ForeignKey(DealOld, on_delete=models.CASCADE, related_name="+")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="+")

    class Meta:
        managed = False
        db_table = "landmatrix_deal_top_investors"

    def __str__(self):
        return f"#{self.deal_id} - {self.investor.name}"
