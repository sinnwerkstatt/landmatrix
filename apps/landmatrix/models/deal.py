from __future__ import annotations

import json

from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Count, F, Sum
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
from .fields import ArrayField, ContractsField, DatasourcesField, LocationsField
from .investor import Investor


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
                current_negotiation_status__in=["ORAL_AGREEMENT", "CONTRACT_SIGNED"]
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
        related_name="deals",
    )
    intended_size = models.DecimalField(
        _("Intended size (in ha)"),
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
        models.CharField(max_length=100, choices=choices.NATURE_OF_DEAL_CHOICES),
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
        max_length=100,
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
        max_length=100,
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
    project_name = models.CharField(
        _("Name of investment project"), max_length=255, blank=True
    )
    investment_chain_comment = models.TextField(
        _("Comment on investment chain"), blank=True
    )

    """ Data sources """
    datasources = DatasourcesField(_("Data sources"), default=list, blank=True)

    """ Local communities / indigenous peoples """
    name_of_community = ArrayField(
        models.CharField(max_length=255, blank=True),
        verbose_name=_("Name of community"),
        blank=True,
        null=True,
    )
    name_of_indigenous_people = ArrayField(
        models.CharField(max_length=255, blank=True),
        verbose_name=_("Name of indigenous people"),
        blank=True,
        null=True,
    )
    people_affected_comment = models.TextField(
        _("Comment on communities / indigenous peoples affected"), blank=True
    )

    recognition_status = ArrayField(
        models.CharField(max_length=100, choices=choices.RECOGNITION_STATUS_CHOICES),
        verbose_name=_("Recognition status of community land tenure"),
        blank=True,
        null=True,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognition status of community land tenure"), blank=True
    )
    community_consultation = models.CharField(
        _("Community consultation"),
        max_length=100,
        choices=choices.COMMUNITY_CONSULTATION_CHOICES,
        blank=True,
        null=True,
    )
    community_consultation_comment = models.TextField(
        _("Comment on consultation of local community"), blank=True
    )

    community_reaction = models.CharField(
        _("Community reaction"),
        max_length=100,
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
        models.CharField(max_length=100, choices=choices.NEGATIVE_IMPACTS_CHOICES),
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
        models.CharField(max_length=100, choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Promised benefits for local communities"),
        blank=True,
        null=True,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    materialized_benefits = ArrayField(
        models.CharField(max_length=100, choices=choices.BENEFITS_CHOICES),
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
        models.CharField(max_length=100, choices=choices.FORMER_LAND_OWNER_CHOICES),
        verbose_name=_("Former land owner"),
        blank=True,
        null=True,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )

    former_land_use = ArrayField(
        models.CharField(max_length=100, choices=choices.FORMER_LAND_USE_CHOICES),
        verbose_name=_("Former land use"),
        blank=True,
        null=True,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )

    former_land_cover = ArrayField(
        models.CharField(max_length=100, choices=choices.FORMER_LAND_COVER_CHOICES),
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
        models.CharField(max_length=100, choices=choices.WATER_SOURCE_CHOICES),
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


class Deal(AbstractDealBase):
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
        max_length=100, blank=True, choices=choices.NOT_PUBLIC_REASON_CHOICES
    )
    parent_companies = models.ManyToManyField(
        Investor, verbose_name=_("Parent companies"), related_name="child_deals"
    )
    top_investors = models.ManyToManyField(
        Investor, verbose_name=_("Top parent companies"), related_name="+"
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
        models.CharField(max_length=100, choices=choices.INTENTION_CHOICES),
        blank=True,
        null=True,
    )
    current_negotiation_status = models.CharField(
        choices=choices.NEGOTIATION_STATUS_CHOICES,
        max_length=100,
        blank=True,
        null=True,
    )
    current_implementation_status = models.CharField(
        choices=choices.IMPLEMENTATION_STATUS_CHOICES,
        max_length=100,
        blank=True,
        null=True,
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

    def recalculate_fields(self, independent=True, dependent=True):
        if independent:
            self.current_contract_size = self._get_current(self.contract_size, "area")
            self.current_production_size = self._get_current(
                self.production_size, "area"
            )
            self.current_intention_of_investment = self._get_current(
                self.intention_of_investment, "choices", multi=True
            )
            self.current_negotiation_status = self._get_current(
                self.negotiation_status, "choice"
            )
            self.current_implementation_status = self._get_current(
                self.implementation_status, "choice"
            )
            self.current_crops = self._get_current(self.crops, "choices", multi=True)
            self.current_animals = self._get_current(
                self.animals, "choices", multi=True
            )
            self.current_mineral_resources = self._get_current(
                self.mineral_resources, "choices", multi=True
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
        # weird hack to deal with https://git.sinntern.de/landmatrix/landmatrix/-/issues/446#note_27505
        ocomp = obj.operating_company_id
        obj.operating_company_id = None
        obj.save()
        obj.operating_company_id = ocomp
        obj.save()
        return obj

    def _get_current(self, attributes, field, multi=False):
        if not attributes:
            return None
        if multi:
            currents = []
            for attr in attributes:
                if attr.get("current") and (values := attr.get(field)):
                    currents += values
            return currents or None
        # prioritize "current" checkbox if present
        current = [x for x in attributes if x.get("current")]
        if current:
            return current[0].get(field)
        else:
            print(self)
            print(attributes)
            raise ValidationError('At least one value needs to be "current".')

    def _calculate_deal_size(self):
        negotiation_status = self.current_negotiation_status
        if not negotiation_status:
            return 0

        intended_size = self.intended_size or 0.0
        contract_size = self.current_contract_size or 0.0
        production_size = self.current_production_size or 0.0

        if (
            negotiation_status
            in (
                "EXPRESSION_OF_INTEREST",
                "UNDER_NEGOTIATION",
                "MEMORANDUM_OF_UNDERSTANDING",
            )
            or negotiation_status == "NEGOTIATIONS_FAILED"
        ):
            value = intended_size or contract_size or production_size
        elif (
            negotiation_status
            in (
                "ORAL_AGREEMENT",
                "CONTRACT_SIGNED",
                "CHANGE_OF_OWNERSHIP",
            )
            or negotiation_status == "CONTRACT_CANCELED"
            or negotiation_status == "CONTRACT_EXPIRED"
        ):
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

    def _calculate_transnational(self) -> bool | None:
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
        for loc in self.locations or []:  # type: dict
            if loc.get("point"):
                features += [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [loc["point"]["lng"], loc["point"]["lat"]],
                        },
                        "properties": {
                            "type": "point",
                            "id": loc["id"],
                            "name": loc.get("name"),
                            "spatial_accuracy": loc.get("level_of_accuracy"),
                        },
                    }
                ]
            areas = loc.get("areas")
            if areas:
                feats = areas["features"]
                for feat in feats:
                    feat["properties"]["name"] = loc.get("name")
                    feat["properties"]["id"] = loc["id"]
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

    @classmethod
    def get_geo_markers(cls, region_id=None, country_id=None):
        region_coordinates = {
            2: [6.06433, 17.082249],
            9: [-22.7359, 140.0188],
            21: [54.526, -105.2551],
            142: [34.0479, 100.6197],
            150: [52.0055, 37.9587],
            419: [-4.442, -61.3269],
        }
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
            all_geojson = list(
                deals.filter(country_id=country_id)
                .exclude(geojson=None)
                .values_list("geojson", flat=True)
            )
            markers = []
            for deal_geojson in all_geojson:
                markers += [
                    {"coordinates": list(reversed(feature["geometry"]["coordinates"]))}
                    for feature in deal_geojson.get("features", [])
                    if feature["geometry"]["type"] == "Point"
                ]
            return markers

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

    # WARNING
    # Do not use to map large query sets!
    # Takes tons of memory storing related deal and deal_version objects.
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
