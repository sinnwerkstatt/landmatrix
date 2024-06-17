import json
import re
from enum import Enum

from django_pydantic_field import SchemaField
from nanoid import generate

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.contrib.gis.geos.prototypes.io import wkt_w
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Case, Count, F, Func, Q, QuerySet, Value, When
from django.db.models.functions import Concat, JSONObject
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError, PermissionDenied
from wagtail.models import Site

from apps.accounts.models import User, UserRole
from apps.landmatrix.models import choices, schema
from apps.landmatrix.models.choices import NatureOfDealEnum
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.fields import (
    ArrayField,
    ChoiceArrayField,
    DecimalIntField,
    LooseDateField,
    NanoIDField,
)

VERSION_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("REVIEW", _("Review")),
    ("ACTIVATION", _("Activation")),
    ("ACTIVATED", _("Activated")),
)


class DealVersionBaseFields(models.Model):
    deal = models.ForeignKey(
        "DealHull", on_delete=models.PROTECT, related_name="versions"
    )

    # """ Locations """
    # via Foreignkey

    """ General info """
    # Land area
    intended_size = DecimalIntField(
        _("Intended size"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contract_size = SchemaField(
        schema=schema.CurrentDateAreaSchema, blank=True, default=list
    )
    production_size = SchemaField(
        schema=schema.CurrentDateAreaSchema, blank=True, default=list
    )
    land_area_comment = models.TextField(_("Comment on land area"), blank=True)

    # Intention of investment
    intention_of_investment = SchemaField(
        schema=schema.CurrentDateAreaChoicesIOI, blank=True, default=list
    )
    intention_of_investment_comment = models.TextField(
        _("Comment on intention of investment"), blank=True
    )

    # Carbon offset project
    carbon_offset_project = models.BooleanField(null=True, blank=True)
    carbon_offset_project_comment = models.TextField(blank=True)

    # Nature of the deal
    nature_of_deal = ChoiceArrayField(
        models.CharField(choices=choices.NATURE_OF_DEAL_CHOICES),
        verbose_name=_("Nature of the deal"),
        blank=True,
        default=list,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"), blank=True
    )

    # # Negotiation status
    negotiation_status = SchemaField(
        schema=schema.CurrentDateChoiceNegotiationStatus,
        blank=True,
        default=list,
    )
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"), blank=True
    )

    # # Implementation status
    implementation_status = SchemaField(
        schema=schema.CurrentDateChoiceImplementationStatus,
        blank=True,
        default=list,
    )
    implementation_status_comment = models.TextField(
        _("Comment on implementation status"), blank=True
    )

    # Purchase price
    purchase_price = DecimalIntField(
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
        choices=choices.HaAreasEnum,
        blank=True,
        null=True,
    )
    purchase_price_area = DecimalIntField(
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
    annual_leasing_fee = DecimalIntField(
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
        choices=choices.HaAreasEnum,
        blank=True,
        null=True,
    )
    annual_leasing_fee_area = DecimalIntField(
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
    # models.CharField(choices=YES_IN_PLANNING_NO_CHOICES)
    contract_farming = models.BooleanField(null=True)

    on_the_lease_state = models.BooleanField(_("On leased / purchased"), null=True)
    on_the_lease = SchemaField(schema=schema.LeaseSchema, blank=True, default=list)

    off_the_lease_state = models.BooleanField(
        _("Not on leased / purchased (out-grower)"), null=True
    )
    off_the_lease = SchemaField(schema=schema.LeaseSchema, blank=True, default=list)
    contract_farming_comment = models.TextField(
        _("Comment on contract farming"), blank=True
    )

    # """ Contracts """
    # via Foreignkey

    """ Employment """
    total_jobs_created = models.BooleanField(_("Jobs created (total)"), null=True)
    total_jobs_planned = models.IntegerField(
        _("Planned number of jobs (total)"), blank=True, null=True
    )
    total_jobs_planned_employees = models.IntegerField(
        _("Planned employees (total)"), blank=True, null=True
    )
    total_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (total)"), blank=True, null=True
    )
    total_jobs_current = SchemaField(schema=schema.JobsSchema, blank=True, default=list)
    total_jobs_created_comment = models.TextField(
        _("Comment on jobs created (total)"), blank=True
    )

    foreign_jobs_created = models.BooleanField(_("Jobs created (foreign)"), null=True)
    foreign_jobs_planned = models.IntegerField(
        _("Planned number of jobs (foreign)"), blank=True, null=True
    )
    foreign_jobs_planned_employees = models.IntegerField(
        _("Planned employees (foreign)"), blank=True, null=True
    )
    foreign_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (foreign)"), blank=True, null=True
    )
    foreign_jobs_current = SchemaField(
        schema=schema.JobsSchema, blank=True, default=list
    )
    foreign_jobs_created_comment = models.TextField(
        _("Comment on jobs created (foreign)"), blank=True
    )

    domestic_jobs_created = models.BooleanField(_("Jobs created (domestic)"), null=True)
    domestic_jobs_planned = models.IntegerField(
        _("Planned number of jobs (domestic)"), blank=True, null=True
    )
    domestic_jobs_planned_employees = models.IntegerField(
        _("Planned employees (domestic)"), blank=True, null=True
    )
    domestic_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (domestic)"), blank=True, null=True
    )
    domestic_jobs_current = SchemaField(
        schema=schema.JobsSchema, blank=True, default=list
    )
    domestic_jobs_created_comment = models.TextField(
        _("Comment on jobs created (domestic)"), blank=True
    )

    """ Investor info """
    operating_company = models.ForeignKey(
        "InvestorHull",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dealversions",
    )
    involved_actors = SchemaField(schema=schema.ActorsSchema, blank=True, default=list)
    project_name = models.CharField(_("Name of investment project"), blank=True)
    investment_chain_comment = models.TextField(
        _("Comment on investment chain"), blank=True
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
        _("Comment on communities / indigenous peoples affected"), blank=True
    )

    recognition_status = ChoiceArrayField(
        models.CharField(choices=choices.RECOGNITION_STATUS_CHOICES),
        verbose_name=_("Recognition status of community land tenure"),
        blank=True,
        default=list,
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
        _("Number of people actually displaced"), blank=True, null=True
    )
    displaced_households = models.IntegerField(
        _("Number of households actually displaced"), blank=True, null=True
    )
    displaced_people_from_community_land = models.IntegerField(
        _("Number of people displaced out of their community land"),
        blank=True,
        null=True,
    )
    displaced_people_within_community_land = models.IntegerField(
        _("Number of people displaced staying on community land"), blank=True, null=True
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
        _("Comment on displacement of people"), blank=True
    )

    negative_impacts = ChoiceArrayField(
        models.CharField(choices=choices.NEGATIVE_IMPACTS_CHOICES),
        verbose_name=_("Negative impacts for local communities"),
        blank=True,
        default=list,
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

    promised_benefits = ChoiceArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Promised benefits for local communities"),
        blank=True,
        default=list,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    materialized_benefits = ChoiceArrayField(
        models.CharField(choices=choices.BENEFITS_CHOICES),
        verbose_name=_("Materialized benefits for local communities"),
        blank=True,
        default=list,
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
    former_land_owner = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_OWNER_CHOICES),
        verbose_name=_("Former land owner"),
        blank=True,
        default=list,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )
    former_land_use = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_USE_CHOICES),
        verbose_name=_("Former land use"),
        blank=True,
        default=list,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )
    former_land_cover = ChoiceArrayField(
        models.CharField(choices=choices.FORMER_LAND_COVER_CHOICES),
        verbose_name=_("Former land cover"),
        blank=True,
        default=list,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"), blank=True
    )

    """ Produce info """
    crops = SchemaField(schema=schema.ExportsCrops, blank=True, default=list)
    crops_comment = models.TextField(_("Comment on crops"), blank=True)

    animals = SchemaField(schema=schema.ExportsAnimals, blank=True, default=list)
    animals_comment = models.TextField(_("Comment on livestock"), blank=True)

    mineral_resources = SchemaField(
        schema=schema.ExportsMineralResources, blank=True, default=list
    )
    mineral_resources_comment = models.TextField(
        _("Comment on mineral resources"), blank=True
    )

    contract_farming_crops = SchemaField(
        schema=schema.CurrentDateAreaChoicesCrops,
        blank=True,
        default=list,
    )
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"), blank=True
    )
    contract_farming_animals = SchemaField(
        schema=schema.CurrentDateAreaChoicesAnimals,
        blank=True,
        default=list,
    )
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"), blank=True
    )

    electricity_generation = SchemaField(
        schema=schema.ElectricityGenerationSchema, blank=True, default=list
    )
    electricity_generation_comment = models.TextField(
        _("Comment on electricity generation"), blank=True
    )
    carbon_sequestration = SchemaField(
        schema=schema.CarbonSequestrationSchema, blank=True, default=list
    )
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
            "Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)"
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

    source_of_water_extraction = ChoiceArrayField(
        models.CharField(choices=choices.WATER_SOURCE_CHOICES),
        verbose_name=_("Source of water extraction"),
        blank=True,
        default=list,
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


class BaseVersionMixin(models.Model):
    created_at = models.DateTimeField(_("Created at"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Modified at"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_review_at = models.DateTimeField(
        _("Sent to review at"), null=True, blank=True
    )
    sent_to_review_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_activation_at = models.DateTimeField(
        _("Reviewed at"), null=True, blank=True
    )
    sent_to_activation_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    activated_at = models.DateTimeField(_("Activated at"), null=True, blank=True)
    activated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    status = models.CharField(choices=VERSION_STATUS_CHOICES, default="DRAFT")

    def save(self, *args, **kwargs):
        if self._state.adding and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def change_status(
        self,
        new_status: str,
        user: User,
        to_user_id: int = None,
    ):
        if new_status == "TO_REVIEW":
            if not (self.created_by == user or user.role >= UserRole.EDITOR):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "REVIEW"
            self.sent_to_review_at = timezone.now()
            self.sent_to_review_by = user
            self.save()
        elif new_status == "TO_ACTIVATION":
            if user.role < UserRole.EDITOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "ACTIVATION"
            self.sent_to_activation_at = timezone.now()
            self.sent_to_activation_by = user
            self.save()
        elif new_status == "ACTIVATE":
            if user.role < UserRole.ADMINISTRATOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "ACTIVATED"
            self.activated_at = timezone.now()
            self.activated_by = user
            self.save()
        elif new_status == "TO_DRAFT":
            if user.role < UserRole.EDITOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.copy_to_new_draft(to_user_id)

        else:
            raise ParseError("Invalid transition")

    class Meta:
        abstract = True

    def copy_to_new_draft(self, created_by_id):
        self.id = None
        self.status = "DRAFT"
        self.created_at = timezone.now()
        self.created_by_id = created_by_id
        self.sent_to_review_at = None
        self.sent_to_review_by = None
        self.sent_to_activation_at = None
        self.sent_to_activation_by = None
        self.activated_at = None
        self.activated_by = None


class DealVersion(DealVersionBaseFields, BaseVersionMixin):
    """# CALCULATED FIELDS #"""

    # is_public: change the logic how it's calculated a bit - confidential is dealhull stuff
    is_public = models.BooleanField(default=False)
    has_known_investor = models.BooleanField(default=False)

    # NOTE: Next two fields should have used through keyword.
    parent_companies = models.ManyToManyField(
        "InvestorHull",
        verbose_name=_("Parent companies"),
        related_name="child_deals",
        blank=True,
    )
    # Can be queried via DealTopInvestors view model:
    top_investors = models.ManyToManyField(
        "InvestorHull",
        verbose_name=_("Top parent companies"),
        related_name="+",
        blank=True,
    )
    current_contract_size = DecimalIntField(
        verbose_name=_("Current contract size"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_production_size = DecimalIntField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_intention_of_investment = ChoiceArrayField(
        models.CharField(choices=choices.INTENTION_OF_INVESTMENT_CHOICES),
        blank=True,
        default=list,
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
    current_crops = ArrayField(models.CharField(), blank=True, default=list)
    current_animals = ArrayField(models.CharField(), blank=True, default=list)
    current_mineral_resources = ArrayField(models.CharField(), blank=True, default=list)
    current_electricity_generation = ArrayField(
        models.CharField(), blank=True, default=list
    )
    current_carbon_sequestration = ArrayField(
        models.CharField(), blank=True, default=list
    )

    deal_size = DecimalIntField(max_digits=18, decimal_places=2, blank=True, null=True)
    initiation_year = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1970)]
    )
    forest_concession = models.BooleanField(default=False)
    transnational = models.BooleanField(null=True)

    # META
    fully_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"v{self.id} for #{self.deal_id}"

    def is_current_draft(self):
        return self.deal.draft_version_id == self.id

    @transaction.atomic
    def save(
        self, recalculate_independent=True, recalculate_dependent=True, *args, **kwargs
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
        new_status: str,
        user: User,
        fully_updated=False,
        to_user_id: int = None,
        comment="",
    ):
        old_draft_status = self.status

        super().change_status(new_status=new_status, user=user, to_user_id=to_user_id)

        if new_status == "TO_REVIEW":
            if fully_updated:
                self.fully_updated = True
            self.save()
        elif new_status == "ACTIVATE":
            deal: DealHull = self.deal
            deal.draft_version = None
            deal.active_version = self
            # using "last modified" timestamp for "last fully updated" #681
            if self.fully_updated:
                deal.fully_updated_at = self.modified_at
            deal.save()

            # close unresolved workflowinfos
            self.workflowinfos.all().update(resolved=True)
        elif new_status == "TO_DRAFT":
            self.save()

            deal = self.deal
            deal.draft_version = self
            deal.save()

            # close remaining open feedback requests
            self.workflowinfos.filter(
                Q(status_before__in=["REVIEW", "ACTIVATION"])
                & Q(status_after="DRAFT")
                & (Q(from_user=user) | Q(to_user=user))
            ).update(resolved=True)

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
        self.save(recalculate_dependent=False)

        # copy foreignkey-relations
        l1: Location
        for l1 in old_self.locations.all():
            areas: list[Area] = list(l1.areas.all())
            l1.id = None
            l1.dealversion = self
            l1.save()
            for a1 in areas:
                a1.id = None
                a1.location = l1
                a1.save()
        d1: DealDataSource
        for d1 in old_self.datasources.all():
            d1.id = None
            d1.dealversion = self
            d1.save()
        c1: Contract
        for c1 in old_self.contracts.all():
            c1.id = None
            c1.dealversion = self
            c1.save()

        self.save()

    def __get_current(self, attributes, field, multi=False):
        if not attributes or not attributes.root:
            return None

        if multi:
            currents = []
            for attr in attributes:
                if attr.current and (values := getattr(attr, field)):
                    currents += [
                        val.value if isinstance(val, Enum) else val for val in values
                    ]
            return currents or None

        # prioritize "current" checkbox if present
        current = [x for x in attributes if x.current]

        # ic(current)
        if current:
            val = getattr(current[0], field)
            if isinstance(val, Enum):
                return val.value
            return val
        else:
            print(self)
            print(attributes)
            raise ValidationError('At least one value needs to be "current".')

    def __calculate_parent_companies(self) -> None:
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

    def __calculate_initiation_year(self):
        self.negotiation_status: list
        valid_negotiation_status = (
            [
                int(x.date[:4])
                for x in self.negotiation_status
                if x.date
                and x.choice
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
        self.implementation_status: list
        valid_implementation_status = (
            [
                int(x.date[:4])
                for x in self.implementation_status
                if x.date
                and x.choice
                in (
                    "STARTUP_PHASE",
                    "IN_OPERATION",
                    "PROJECT_ABANDONED",
                )
            ]
            if self.implementation_status
            else []
        )
        dates = valid_implementation_status + valid_negotiation_status
        return min(dates) if dates else None

    def __calculate_forest_concession(self) -> bool:
        return bool(
            self.nature_of_deal
            # TODO: Replace literal with NatureOfDealEnum or enforce type checking on self.nature_of_deal
            and "CONCESSION" in self.nature_of_deal
            and self.current_intention_of_investment
            # TODO: Replace with IntentionOfInvestmentEnum
            and "FOREST_LOGGING" in self.current_intention_of_investment
        )

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
        DealVersion, on_delete=models.CASCADE, related_name="locations"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    level_of_accuracy = models.CharField(
        _("Spatial accuracy level"),
        blank=True,
        choices=choices.LEVEL_OF_ACCURACY_CHOICES,
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

    class Meta:
        # unique_together = ["location", "type", "current"]
        ordering = ["id"]


class Contract(models.Model):
    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="contracts"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    number = models.CharField(_("Contract number"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    expiration_date = LooseDateField(_("Expiration date"), blank=True, null=True)
    agreement_duration = models.IntegerField(
        _("Duration of the agreement"), blank=True, null=True
    )
    comment = models.TextField(_("Comment"), blank=True)

    def to_dict(self):
        return {
            "nid": self.nid,
            "number": self.number,
            "date": self.date,
            "expiration_date": self.expiration_date,
            "agreement_duration": self.agreement_duration,
            "comment": self.comment,
        }

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


class BaseDataSource(models.Model):
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(_("Type"), choices=choices.DATASOURCE_TYPE_CHOICES)
    # NOTE hit a URL > 1000 chars... so going with 5000 for now.
    url = models.URLField(_("Url"), blank=True, max_length=5000)
    file = models.FileField(_("File"), blank=True, null=True, max_length=3000)
    file_not_public = models.BooleanField(_("Keep PDF not public"), default=False)
    publication_title = models.CharField(_("Publication title"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    name = models.CharField(_("Name"), blank=True)
    company = models.CharField(_("Organisation"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), blank=True)
    includes_in_country_verified_information = models.BooleanField(
        _("Includes in-country-verified information"), blank=True, null=True
    )
    open_land_contracts_id = models.CharField(_("Open Contracting ID"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    def to_dict(self):
        return {
            "nid": self.nid,
            "type": self.type,
            "url": self.url,
            "file": str(self.file),
            "file_not_public": self.file_not_public,
            "publication_title": self.publication_title,
            "date": self.date,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "phone": self.phone,
            "includes_in_country_verified_information": self.includes_in_country_verified_information,
            "open_land_contracts_id": self.open_land_contracts_id,
            "comment": self.comment,
        }

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


class DealDataSource(BaseDataSource):
    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="datasources"
    )

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


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


class HullBase(models.Model):
    deleted = models.BooleanField(default=False)
    deleted_comment = models.TextField(blank=True)

    # mainly for management/case_statistics
    first_created_at = models.DateTimeField()
    first_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and not self.first_created_at:
            self.first_created_at = timezone.now()
        super().save(*args, **kwargs)


class DealHull(HullBase):
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deals",
    )

    active_version = models.ForeignKey(
        DealVersion, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    draft_version = models.ForeignKey(
        DealVersion, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )

    confidential = models.BooleanField(default=False)
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True
    )

    # ## calculated
    fully_updated_at = models.DateTimeField(
        _("Last full update"), null=True, blank=True
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

    def add_draft(self, created_by: User = None) -> DealVersion:
        dv = DealVersion.objects.create(deal=self, created_by=created_by)
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


class InvestorVersion(BaseVersionMixin, models.Model):
    investor = models.ForeignKey(
        "InvestorHull", on_delete=models.PROTECT, related_name="versions"
    )

    name = models.CharField(_("Name"), blank=True)
    name_unknown = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    classification = models.CharField(
        verbose_name=_("Classification"),
        choices=choices.INVESTOR_CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
    )

    homepage = models.URLField(_("Investor homepage"), blank=True)
    opencorporates = models.URLField(_("Opencorporates link"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    # """ Data sources """  via Foreignkey

    """ calculated properties """
    involvements_snapshot = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.name} (#{self.id})"

    def is_current_draft(self):
        return self.investor.draft_version_id == self.id

    def save(self, *args, **kwargs):
        self._recalculate_fields()
        super().save(*args, **kwargs)

    def _recalculate_fields(self):
        self.name_unknown = bool(
            re.search(r"(unknown|unnamed)", self.name, re.IGNORECASE)
        )

    def change_status(
        self,
        new_status: str,
        user: User,
        to_user_id: int = None,
        comment="",
    ):
        old_draft_status = self.status

        super().change_status(new_status=new_status, user=user, to_user_id=to_user_id)

        if new_status == "ACTIVATE":
            investor: InvestorHull = self.investor
            investor.draft_version = None
            investor.active_version = self

            # upon activation, map the involvements_snapshot into the Involvements table
            seen_involvements = set()
            for invo in self.involvements_snapshot:
                # involvements include bidirectional relations. we filter out only parent relations that we save.
                if invo["child_investor_id"] != investor.id:
                    continue

                try:
                    assert isinstance(invo["id"], int)
                    i1 = Involvement.objects.get(id=invo["id"], child_investor=investor)
                except (Involvement.DoesNotExist, AssertionError):
                    i1 = Involvement(child_investor=investor)
                i1.parent_investor_id = invo["parent_investor_id"]
                i1.role = invo["role"]
                i1.investment_type = invo["investment_type"]
                i1.percentage = invo["percentage"]
                i1.loans_amount = invo["loans_amount"]
                i1.loans_currency_id = invo["loans_currency_id"]
                i1.loans_date = invo["loans_date"]
                i1.parent_relation = invo["parent_relation"]
                i1.comment = invo["comment"]
                i1.save()
                seen_involvements.add(i1.id)
            Involvement.objects.filter(child_investor=investor).exclude(
                id__in=seen_involvements
            ).delete()

            investor.save()

            # close unresolved workflowinfos
            self.workflowinfos.all().update(resolved=True)
        elif new_status == "TO_DRAFT":
            investor = self.investor
            investor.draft_version = self
            investor.save()

            # close remaining open feedback requests
            self.workflowinfos.filter(
                Q(status_before__in=["REVIEW", "ACTIVATION"])
                & Q(status_after="DRAFT")
                & (Q(from_user=user) | Q(to_user=user))
            ).update(resolved=True)

        InvestorWorkflowInfo.objects.create(
            investor_id=self.investor_id,
            investor_version=self,
            from_user=user,
            to_user_id=to_user_id,
            status_before=old_draft_status,
            status_after=self.status,
            comment=comment,
        )

    def copy_to_new_draft(self, created_by_id: int):
        old_self = InvestorVersion.objects.get(pk=self.pk)

        super().copy_to_new_draft(created_by_id)
        self.save()

        # copy foreignkey-relations
        d1: InvestorDataSource
        for d1 in old_self.datasources.all():
            d1.id = None
            d1.investorversion = self
            d1.save()


class InvestorDataSource(BaseDataSource):
    investorversion = models.ForeignKey(
        InvestorVersion, on_delete=models.CASCADE, related_name="datasources"
    )

    class Meta:
        unique_together = ["investorversion", "nid"]
        indexes = [models.Index(fields=["investorversion", "nid"])]
        ordering = ["id"]


class InvestorHullQuerySet(models.QuerySet):
    def normal(self):
        return self.filter(deleted=False)

    def active(self):
        return self.normal().filter(active_version__isnull=False)

    # NOTE at the moment the only thing we filter on is the "status".
    # the following is an idea:
    # def public(self):
    #     return self.active().filter(is_actually_unknown=False)

    def visible(self, user=None, subset="PUBLIC"):
        if subset in ["ACTIVE", "PUBLIC"]:
            return self.active()

        if not user or not user.is_authenticated:
            return self.active()

        # hand it out unfiltered.
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


class InvestorHull(HullBase):
    active_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    objects = InvestorHullQuerySet.as_manager()

    def __str__(self):
        return f"#{self.id}"

    # This method is used by DRF.
    def selected_version(self):
        if hasattr(self, "_selected_version_id") and self._selected_version_id:
            try:
                return self.versions.get(id=self._selected_version_id)
            except InvestorVersion.DoesNotExist:
                raise Http404
        return self.active_version or self.draft_version

    def add_draft(self, created_by: User = None) -> InvestorVersion:
        dv = InvestorVersion.objects.create(investor=self, created_by=created_by)
        self.draft_version = dv
        self.save()
        return dv

    # This method is used by DRF.
    def involvements(self):
        if not hasattr(self, "_selected_version_id") and self.active_version:
            return Involvement.objects.filter(
                Q(parent_investor_id=self.id) | Q(child_investor_id=self.id)
            )
        return

    def involvements_graph(self, depth, include_deals, show_ventures):
        from apps.landmatrix.involvement_network import InvolvementNetwork

        return InvolvementNetwork().get_network_x(
            self.id, depth, include_deals=include_deals, show_ventures=show_ventures
        )

    def to_list_dict(self):
        """
        should only be called on InvestorHulls filtered by having active_versions
        """
        return {
            "id": self.id,
            "selected_version": {
                "id": self.active_version.id,
                "name": self.active_version.name,
                "modified_at": self.active_version.modified_at,
                "classification": self.active_version.classification,
                "country": {"id": self.active_version.country_id},
            },
        }

    @staticmethod
    def to_investor_list(qs: QuerySet["InvestorHull"]):
        deals = DealHull.objects.filter(
            active_version__operating_company_id__in=qs.values_list("id", flat=True)
        ).values("id", "active_version__operating_company_id")

        return [
            {
                "id": inv["id"],
                "selected_version": inv["selected_version"],
                "deals": [
                    x["id"]
                    for x in deals
                    if x["active_version__operating_company_id"] == inv["id"]
                ],
            }
            for inv in qs.annotate(
                selected_version=JSONObject(
                    id="active_version_id",
                    name="active_version__name",
                    name_unknown="active_version__name_unknown",
                    modified_at="active_version__modified_at",
                    classification="active_version__classification",
                    country_id="active_version__country_id",
                )
            ).values("id", "selected_version")
        ]

    def get_parent_companies(
        self, top_investors_only=False, _seen_investors: set["InvestorHull"] = None
    ) -> set["InvestorHull"]:
        """
        Get list of the highest parent companies
        (all right-hand side parent companies of the network visualisation)
        """
        if _seen_investors is None:
            _seen_investors = {self}

        investor_involvements = (
            Involvement.objects.filter(child_investor=self)
            .filter(
                parent_investor__active_version__isnull=False,
                parent_investor__deleted=False,
            )
            .filter(role="PARENT")
            .exclude(parent_investor__in=_seen_investors)
        )

        self.is_top_investor = not investor_involvements

        for involvement in investor_involvements:
            if involvement.parent_investor in _seen_investors:
                continue
            _seen_investors.add(involvement.parent_investor)
            involvement.parent_investor.get_parent_companies(
                top_investors_only, _seen_investors
            )
        return _seen_investors

    def get_affected_dealversions(self, seen_investors=None) -> set[DealVersion]:
        """
        Get list of affected deals - this is like Top Investors, only downwards
        (all left-hand side deals of the network visualisation)
        """
        deals = set()
        if seen_investors is None:
            seen_investors = {self}

        child_investor_involvements = (
            self.child_investors.active()
            .filter(role="PARENT")
            .exclude(child_investor__in=seen_investors)
        )

        dealv: DealVersion
        for dealv in self.dealversions.filter(id=F("deal__active_version_id")):
            deals.add(dealv)

        for involvement in child_investor_involvements:
            if involvement.child_investor in seen_investors:
                continue
            seen_investors.add(involvement.child_investor)
            deals.update(
                involvement.child_investor.get_affected_dealversions(seen_investors)
            )
        return deals


class InvolvementQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            parent_investor__active_version__isnull=False,
            parent_investor__deleted=False,
            child_investor__active_version__isnull=False,
            child_investor__deleted=False,
        )

    # this is just an idea at this point
    # def public(self):
    #     return self.active().filter(
    #         investor__is_actually_unknown=False,
    #         venture__is_actually_unknown=False,
    #     )

    def visible(self, user=None, subset="PUBLIC"):
        if subset in ["ACTIVE", "PUBLIC"]:
            return self.active()

        if not user or not (user.is_staff or user.is_superuser):
            return self.active()

        # hand it out unfiltered.
        return self


class Involvement(models.Model):
    # TODO: Add nanoId
    # nid = NanoIDField("ID", max_length=15, db_index=True, null=True)
    parent_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Investor"),
        db_index=True,
        related_name="child_investors",
        on_delete=models.PROTECT,
    )
    child_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Venture Company"),
        db_index=True,
        related_name="parent_investors",
        on_delete=models.PROTECT,
    )

    role = models.CharField(
        verbose_name=_("Relation type"), choices=choices.INVOLVEMENT_ROLE_CHOICES
    )

    investment_type = ChoiceArrayField(
        models.CharField(choices=choices.INVESTMENT_TYPE_CHOICES),
        verbose_name=_("Investment type"),
        blank=True,
        default=list,
    )

    percentage = models.DecimalField(
        _("Ownership share"),
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    loans_date = LooseDateField(_("Loan date"), blank=True, null=True)

    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
        choices=choices.PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True)

    objects = InvolvementQuerySet.as_manager()

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["id"]
        # would be nice to have but not today
        # unique_together = [["parent_investor", "child_investor"]]

    def __str__(self):
        if self.role == "PARENT":
            role = _("<is PARENT of>")
        else:
            role = _("<is INVESTOR of>")
        return f"{self.parent_investor} {role} {self.child_investor}"


class _WorkflowInfo(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    status_before = models.CharField(
        choices=VERSION_STATUS_CHOICES, null=True, blank=True
    )
    status_after = models.CharField(
        choices=VERSION_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    replies = models.JSONField(null=True, default=list)
    resolved = models.BooleanField(default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "status_before": self.status_before,
            "status_after": self.status_after,
            "timestamp": self.timestamp,
            "comment": self.comment,
            "resolved": self.resolved,
            "replies": self.replies,
        }

    def get_object_url(self):
        _site = Site.objects.get(is_default_site=True)
        _port = f":{_site.port}" if _site.port not in [80, 443] else ""
        base_url = f"http{'s' if _site.port == 443 else ''}://{_site.hostname}{_port}"
        return base_url

    class Meta:
        abstract = True


class DealWorkflowInfo(_WorkflowInfo):
    deal = models.ForeignKey(
        DealHull, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    deal_version = models.ForeignKey(
        DealVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    # OLD Code
    # # WARNING
    # # Do not use to map large query sets!
    # # Takes tons of memory storing related deal and deal_version objects.
    # def to_dict(self) -> dict:
    #     d = super().to_dict()
    #     d.update({"deal": self.deal, "deal_version": self.deal_version})
    #     return d

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"deal_id": self.deal_id, "deal_version_id": self.deal_version_id})
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/deal/{self.deal_id}/"


class InvestorWorkflowInfo(_WorkflowInfo):
    investor = models.ForeignKey(
        InvestorHull, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    investor_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "investor_id": self.investor_id,
                "investor_version_id": self.investor_version_id,
            }
        )
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/investor/{self.investor_id}/"


class DealTopInvestors(models.Model):
    """A view on dealversion.top_investors M2M relation table."""

    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="+"
    )
    investorhull = models.ForeignKey(
        InvestorHull, on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        managed = False
        db_table = "landmatrix_dealversion_top_investors"

    def __str__(self):
        return f"#{self.dealversion.deal_id} - {self.investorhull.active_version.name}"
