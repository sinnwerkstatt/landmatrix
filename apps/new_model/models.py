import json
import re

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from icecream import ic

from apps.landmatrix.models import choices
from apps.landmatrix.models.choices import (
    DATASOURCE_TYPE_CHOICES,
    LEVEL_OF_ACCURACY_CHOICES,
    NEGOTIATION_STATUS_ITEMS,
    IMPLEMENTATION_STATUS_ITEMS,
    INTENTION_OF_INVESTMENT_ITEMS,
    CROPS_ITEMS,
    ANIMALS_ITEMS,
    MINERALS_ITEMS,
    INVESTMENT_TYPE_ITEMS,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import AbstractDealBase
from apps.landmatrix.models.fields import (
    JSONCurrentDateAreaField,
    JSONCurrentDateChoiceField,
    JSONCurrentDateAreaChoicesField,
    ChoiceArrayField,
    ArrayField,
    JSONLeaseField,
    JSONJobsField,
    JSONActorsField,
    JSONExportsField,
    NanoIDField,
    LooseDateField,
    JSONCarbonSequestrationField,
    JSONElectricityGenerationField,
    DecimalIntField,
)
from apps.landmatrix.models.investor import Investor
from apps.new_model.utils import InvolvementNetwork
from django.contrib.gis.geos.prototypes.io import wkt_w

DRAFT_STATUS = {
    "DRAFT": 1,
    "REVIEW": 2,
    "ACTIVATION": 3,
    "ACTIVATED": 4,
    # TODO: old, can probably remove?
    "REJECTED": -1,
    "TO_DELETE": -2,
}
DRAFT_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("REVIEW", _("Review")),
    ("ACTIVATION", _("Activation")),
    ("ACTIVATED", _("Activated")),
    # TODO: old, can probably remove?
    ("REJECTED", _("OLD: Rejected")),
    ("TO_DELETE", _("OLD: To Delete")),
)
VERSION_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("REVIEW", _("Review")),
    ("ACTIVATION", _("Activation")),
    ("ACTIVATED", _("Activated")),
    # TODO: old, can probably remove?
    ("REJECTED", _("OLD: Rejected")),
    ("TO_DELETE", _("OLD: To Delete")),
)


class DealVersionBaseFields(models.Model):
    deal = models.ForeignKey(
        "new_model.DealHull", on_delete=models.PROTECT, related_name="versions"
    )

    # """ Locations """
    # via Foreignkey

    """ General info """
    # Land area
    intended_size = DecimalIntField(
        _("Intended size (in ha)"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    contract_size = JSONCurrentDateAreaField(blank=True, default=list)
    production_size = JSONCurrentDateAreaField(blank=True, default=list)
    land_area_comment = models.TextField(_("Comment on land area"), blank=True)

    # Intention of investment
    intention_of_investment = JSONCurrentDateAreaChoicesField(
        blank=True,
        default=list,
        choices=[x["value"] for x in INTENTION_OF_INVESTMENT_ITEMS],
    )
    intention_of_investment_comment = models.TextField(
        _("Comment on intention of investment"), blank=True
    )

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
    negotiation_status = JSONCurrentDateChoiceField(
        verbose_name=_("Negotiation status"),
        blank=True,
        default=list,
        choices=[x["value"] for x in NEGOTIATION_STATUS_ITEMS],
    )
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"), blank=True
    )

    # # Implementation status
    implementation_status = JSONCurrentDateChoiceField(
        verbose_name=_("Implementation status"),
        blank=True,
        default=list,
        choices=[x["value"] for x in IMPLEMENTATION_STATUS_ITEMS],
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
        choices=choices.HA_AREA_CHOICES,
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
        choices=choices.HA_AREA_CHOICES,
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
    on_the_lease = JSONLeaseField(blank=True, default=list)

    off_the_lease_state = models.BooleanField(
        _("Not on leased / purchased (out-grower)"), null=True
    )
    off_the_lease = JSONLeaseField(blank=True, default=list)

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
    total_jobs_current = JSONJobsField(blank=True, default=list)
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
    foreign_jobs_current = JSONJobsField(blank=True, default=list)
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
    domestic_jobs_current = JSONJobsField(blank=True, default=list)
    domestic_jobs_created_comment = models.TextField(
        _("Comment on jobs created (domestic)"), blank=True
    )

    """ Investor info """
    operating_company = models.ForeignKey(
        "new_model.InvestorVersion2",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dealversions",
    )
    involved_actors = JSONActorsField(blank=True, default=list)
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
    crops = JSONExportsField(
        verbose_name=_("Crops area/yield/export"),
        blank=True,
        default=list,
        choices=[x["value"] for x in CROPS_ITEMS],
    )
    crops_comment = models.TextField(_("Comment on crops"), blank=True)

    animals = JSONExportsField(
        verbose_name=_("Livestock area/yield/export"),
        blank=True,
        default=list,
        choices=[x["value"] for x in ANIMALS_ITEMS],
    )
    animals_comment = models.TextField(_("Comment on livestock"), blank=True)

    mineral_resources = JSONExportsField(
        verbose_name=_("Mineral resources area/yield/export"),
        blank=True,
        default=list,
        choices=[x["value"] for x in MINERALS_ITEMS],
    )
    mineral_resources_comment = models.TextField(
        _("Comment on mineral resources"), blank=True
    )

    contract_farming_crops = JSONCurrentDateAreaChoicesField(
        blank=True,
        default=list,
        choices=[x["value"] for x in CROPS_ITEMS],
    )
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"), blank=True
    )
    contract_farming_animals = JSONCurrentDateAreaChoicesField(
        blank=True,
        default=list,
        choices=[x["value"] for x in ANIMALS_ITEMS],
    )
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"), blank=True
    )

    electricity_generation = JSONElectricityGenerationField(
        verbose_name=_("Electricity generation"), blank=True, default=list
    )
    electricity_generation_comment = models.TextField(
        _("Comment on electricity generation"), blank=True
    )
    carbon_sequestration = JSONCarbonSequestrationField(
        verbose_name=_("Carbon Sequestration"), blank=True, default=list
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


# class DealVersionQuerySet(models.QuerySet):
#     def active(self):
#         return self.filter(deal__in=DealHull.objects.active())
#
#     def public(self):
#         return self.active().filter(is_public=True)
#
#     def visible(self, user=None, subset="PUBLIC"):
#         # TODO: welche user duerfen unfiltered bekommen?
#         if not user or not user.is_authenticated:
#             return self.public()
#
#         if subset == "PUBLIC":
#             return self.public()
#         elif subset == "ACTIVE":
#             return self.active()
#         return self


class VersionTimestampsMixins(models.Model):
    created_at = models.DateTimeField(_("Created at"), blank=True)
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
    reviewed_at = models.DateTimeField(_("Reviewed at"), null=True, blank=True)
    reviewed_by = models.ForeignKey(
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

    class Meta:
        abstract = True


class DealVersion2(DealVersionBaseFields, VersionTimestampsMixins):

    """# CALCULATED FIELDS #"""

    # is_public: change the logic how it's calculated a bit - confidential is dealhull stuff
    is_public = models.BooleanField(default=False)
    has_known_investor = models.BooleanField(default=False)
    parent_companies = models.ManyToManyField(
        Investor,
        verbose_name=_("Parent companies"),
        related_name="newModel_child_deals",
        blank=True,
    )
    top_investors = models.ManyToManyField(
        Investor,
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
        models.CharField(choices=choices.INTENTION_CHOICES),
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

    deal_size = DecimalIntField(
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

    # META
    fully_updated = models.BooleanField(default=False)
    status = models.CharField(choices=VERSION_STATUS_CHOICES, default="DRAFT")

    def __str__(self):
        return f"v{self.id} for #{self.deal_id}"

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

    def _calculate_parent_companies(self) -> None:
        pass
        # TODO
        # if self.operating_company_id:
        #     oc = Investor.objects.filter(
        #         id=self.operating_company_id,
        #         status__in=[STATUS["LIVE"], STATUS["UPDATED"]],
        #     ).first()
        #     if oc:
        #         parent_companies = oc.get_parent_companies()
        #         self.parent_companies.set(parent_companies)
        #         top_inv = [x for x in parent_companies if x.is_top_investor]
        #         self.top_investors.set(top_inv)
        #         return
        # if self.id:
        #     self.parent_companies.set([])
        #     self.top_investors.set([])

    # def _calculate_public_state(self) -> str:
    #     """
    #     :return: A string with a value if not public, or empty if public
    #     """
    #     if self.confidential:
    #         # 1. Flag "confidential"
    #         return "CONFIDENTIAL"
    #     if not self.country_id:
    #         # No Country
    #         return "NO_COUNTRY"
    #     # the following Country query is intentional. it has to do with country not
    #     # neccessarily being set, when country_id is set.
    #     if Country.objects.get(id=self.country_id).high_income:
    #         # High Income Country
    #         return "HIGH_INCOME_COUNTRY"
    #     if not self.datasources:
    #         # No DataSource
    #         return "NO_DATASOURCES"
    #     if not self.operating_company_id:
    #         # 3. No operating company
    #         return "NO_OPERATING_COMPANY"
    #     if not self.has_known_investor:
    #         # 4. Unknown operating company AND no known operating company parents
    #         return "NO_KNOWN_INVESTOR"
    #     return ""
    def _has_no_known_investor(self) -> bool:
        if not self.operating_company_id:
            return True
        oc = InvestorVersion2.objects.get(id=self.operating_company_id)
        # if the Operating Company is known, we have a known investor and exit.
        if not oc.is_actually_unknown:
            return False
        # only if no known Investor exists, we return True
        return not oc.investors.filter(investor__is_actually_unknown=False).exists()

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
        self.negotiation_status: list
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
        self.implementation_status: list
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
        if not self.deal.country_id:
            # unknown if we have no target country
            return None

        # by definition True, if no operating company exists (or it is deleted)
        if not self.operating_company_id:
            return True
        oc = Investor.objects.get(id=self.operating_company_id)
        # TODO status-deleted?
        # if oc.status == STATUS["DELETED"]:
        #     return True

        investors_countries = self.parent_companies.exclude(
            country_id=None
        ).values_list("country_id", flat=True)

        if not len(investors_countries):
            # treat deals without investors as transnational
            # treat deals without investor countries as transnational
            return True
        # `True` if we have investors in other countries else `False`
        return bool(set(investors_countries) - {self.deal.country_id})

    def recalculate_fields(self, independent=True, dependent=True):
        if independent:
            self.current_contract_size = self._get_current(self.contract_size, "area")
            self.current_production_size = self._get_current(
                self.production_size, "area"
            )
            self.current_intention_of_investment = (
                self._get_current(self.intention_of_investment, "choices", multi=True)
                or []
            )
            self.current_negotiation_status = self._get_current(
                self.negotiation_status, "choice"
            )
            self.current_implementation_status = self._get_current(
                self.implementation_status, "choice"
            )
            self.current_crops = (
                self._get_current(self.crops, "choices", multi=True) or []
            )
            self.current_animals = (
                self._get_current(self.animals, "choices", multi=True) or []
            )
            self.current_mineral_resources = (
                self._get_current(self.mineral_resources, "choices", multi=True) or []
            )
            self.current_electricity_generation = (
                self._get_current(self.electricity_generation, "choices", multi=True)
                or []
            )
            self.current_carbon_sequestration = (
                self._get_current(self.carbon_sequestration, "choices", multi=True)
                or []
            )

            # these only depend on the _get_current calls right above.
            self.deal_size = self._calculate_deal_size()
            self.initiation_year = self._calculate_initiation_year()
            self.forest_concession = self._calculate_forest_concession()
        if dependent:
            # With the help of signals these fields are recalculated on changes to:
            # Investor and InvestorVentureInvolvement
            self.has_known_investor = not self._has_no_known_investor()
            # TODO public state for version. to be discussed
            # self.not_public_reason = self._calculate_public_state()
            # self.is_public = self.not_public_reason == ""

            # this might error because it's m2m, and we need the
            # Deal to have an ID first before we can save the investors. 🙄
            self._calculate_parent_companies()
            self.transnational = self._calculate_transnational()

    @transaction.atomic
    def save(
        self, recalculate_independent=True, recalculate_dependent=True, *args, **kwargs
    ):
        self.recalculate_fields(recalculate_independent, recalculate_dependent)
        super().save(*args, **kwargs)


class Location(models.Model):
    dealversion = models.ForeignKey(
        DealVersion2, on_delete=models.CASCADE, related_name="locations"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    name = models.CharField(_("Location"), blank=True)
    description = models.TextField(_("Description"), blank=True)
    point = gis_models.PointField(_("Point"), blank=True, null=True)
    facility_name = models.CharField(_("Facility name"), blank=True)
    level_of_accuracy = models.CharField(
        _("Spatial accuracy level"),
        blank=True,
        choices=LEVEL_OF_ACCURACY_CHOICES,
    )
    comment = models.TextField(_("Comment"), blank=True)

    def to_dict(self):
        return {
            "nid": self.nid,
            "name": self.name,
            "description": self.description,
            "point": json.loads(self.point.geojson) if self.point else None,
            "facility_name": self.facility_name,
            "level_of_accuracy": self.level_of_accuracy,
            "comment": self.comment,
            "areas": [area.to_dict() for area in self.areas.all()],
        }

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]

    def __str__(self):
        return f"{self.nid} @ {self.dealversion}"


class Area(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="areas"
    )
    AREA_TYPE_CHOICES = (
        ("production_area", _("Production area")),
        ("contract_area", _("Contract area")),
        ("intended_area", _("Intended area")),
    )
    type = models.CharField(choices=AREA_TYPE_CHOICES)
    current = models.BooleanField(default=False)
    date = LooseDateField(_("Date"), blank=True, null=True)
    area = gis_models.GeometryField()

    def __str__(self):
        return f"{self.location} >> {self.type}"

    def to_dict(self):
        return {
            "type": self.type,
            "current": self.current,
            "date": self.date,
            "area": json.loads(self.area.geojson) if self.area else None,
        }

    @staticmethod
    def _remove_third_dimension_on_gis(gis_obj: GEOSGeometry):
        if not gis_obj:
            return gis_obj
        if gis_obj.hasz:
            wkt = wkt_w(dim=2).write(gis_obj).decode()
            gis_obj = GEOSGeometry(wkt, srid=4674)
        return gis_obj

    def save(self, *args, **kwargs):
        self.area = self._remove_third_dimension_on_gis(self.area)
        super().save(*args, **kwargs)

    # class Meta:
    #     unique_together = ["location", "type", "current"]


class Contract(models.Model):
    dealversion = models.ForeignKey(
        DealVersion2, on_delete=models.CASCADE, related_name="contracts"
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

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]


class BaseDataSource(models.Model):
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(_("Type"), choices=DATASOURCE_TYPE_CHOICES, blank=True)
    # NOTE hit a URL > 1000 chars... so going with 2000 for now. TODO this is just ridiculous
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

    class Meta:
        abstract = True
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]


class DealDataSource(BaseDataSource):
    dealversion = models.ForeignKey(
        DealVersion2, on_delete=models.CASCADE, related_name="datasources"
    )

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]


class DealHullQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            active_version__isnull=False, deleted=False, confidential=False
        )

    def public(self):
        return self.active().filter(active_version__is_public=True)

    def visible(self, user=None, subset="PUBLIC"):
        # TODO: welche user duerfen unfiltered bekommen?
        if not user or not user.is_authenticated:
            return self.public()

        if subset == "PUBLIC":
            return self.public()
        elif subset == "ACTIVE":
            return self.active()
        return self


class DealHull(models.Model):
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="newModel_dealHulls",
    )

    active_version = models.ForeignKey(
        DealVersion2, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    draft_version = models.ForeignKey(
        DealVersion2, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )

    confidential = models.BooleanField(default=False)
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True
    )
    deleted = models.BooleanField(default=False)
    deleted_comment = models.TextField(
        _("Comment why this deal is deleted"), blank=True
    )

    # ## calculated
    # this just mirrors the created_at/by from the first version.
    created_at = models.DateTimeField(_("Created"), default=timezone.now, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    fully_updated_at = models.DateTimeField(
        _("Last full update"), null=True, blank=True
    )

    objects = DealHullQuerySet.as_manager()

    def __str__(self):
        if self.country:
            return f"#{self.id} in {self.country.name}"
        return f"#{self.id}"

    def selected_version(self):
        if hasattr(self, "_selected_version_id"):
            return self.versions.get(id=self._selected_version_id)
        return self.active_version or self.draft_version


class InvestorVersion2(VersionTimestampsMixins, models.Model):
    investor = models.ForeignKey(
        "new_model.InvestorHull", on_delete=models.PROTECT, related_name="versions"
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

    status = models.CharField(choices=VERSION_STATUS_CHOICES, default="DRAFT")

    """ calculated properties """
    involvements_snapshot = models.JSONField(blank=True, null=True)

    def recalculate_fields(self):
        # TODO create involvements_snapshot
        pass

    def save(self, *args, **kwargs):
        self.recalculate_fields()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (#{self.id})"


class InvestorDataSource(BaseDataSource):
    investorversion = models.ForeignKey(
        InvestorVersion2, on_delete=models.PROTECT, related_name="datasources"
    )

    class Meta:
        unique_together = ["investorversion", "nid"]
        indexes = [models.Index(fields=["investorversion", "nid"])]


class InvestorHull(models.Model):
    active_version = models.ForeignKey(
        InvestorVersion2,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        InvestorVersion2,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    deleted = models.BooleanField(default=False)
    deleted_comment = models.TextField(
        _("Comment why this investor is deleted"), blank=True
    )

    # ## calculated
    # this just mirrors the created_at/by from the first version.
    created_at = models.DateTimeField(_("Created"), default=timezone.now, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )

    def __str__(self):
        return f"Investor #{self.id}"

    # This method is used by DRF.
    def selected_version(self):
        if hasattr(self, "_selected_version_id"):
            return self.versions.get(id=self._selected_version_id)
        return self.active_version or self.draft_version

    # This method is used by DRF.
    def involvements(self):
        if not hasattr(self, "_selected_version_id") and self.active_version:
            return Involvement.objects.filter(
                Q(parent_investor_id=self.id) | Q(child_investor_id=self.id)
            )
        return

    def involvements_graph(self, depth, include_deals):
        return InvolvementNetwork().get_network(
            self.id, depth, include_deals=include_deals
        )


class Involvement(models.Model):
    # parent_investor_id = models.IntegerField()
    # child_investor_id = models.IntegerField()
    parent_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Investor"),
        db_index=True,
        related_name="ventures",
        on_delete=models.PROTECT,
    )
    child_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Venture Company"),
        db_index=True,
        related_name="investors",
        on_delete=models.PROTECT,
    )

    role = models.CharField(
        verbose_name=_("Relation type"),
        choices=(
            ("PARENT", _("Parent company")),
            ("LENDER", _("Tertiary investor/lender")),
        ),
    )

    investment_type = ChoiceArrayField(
        models.CharField(
            choices=[(x["value"], x["label"]) for x in INVESTMENT_TYPE_ITEMS]
        ),
        verbose_name=_("Investment type"),
        blank=True,
        default=list,
    )

    percentage = models.FloatField(
        _("Ownership share"),
        blank=True,
        null=True,
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
    loans_date = LooseDateField(_("Loan date"), blank=True)

    PARENT_RELATION_CHOICES = (
        ("SUBSIDIARY", _("Subsidiary of parent company")),
        ("LOCAL_BRANCH", _("Local branch of parent company")),
        ("JOINT_VENTURE", _("Joint venture of parent companies")),
    )
    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
        choices=PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True)

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["-id"]

    # def __str__(self):
    #     if self.role == "PARENT":
    #         role = _("<is PARENT of>")
    #     else:
    #         role = _("<is INVESTOR of>")
    #     return f"{self.investor} {role} {self.venture}"

    def to_dict(self, target_id=None):
        relationship = self.role
        other_investor = None
        if target_id is None:
            pass
        elif self.parent_investor_id == target_id:
            relationship = (
                _("Subsidiary company")
                if self.role == "PARENT"
                else _("Beneficiary company")
            )
            other_investor = self.child_investor
        elif self.child_investor_id == target_id:
            relationship = (
                _("Parent company")
                if self.role == "PARENT"
                else _("Tertiary investor/lender")
            )
            other_investor = self.parent_investor
        else:
            pass

        other_investor_dict = (
            {
                "id": other_investor.id,
                "name": other_investor.active_version.name
                if other_investor.active_version
                else None,
                "country": {"id": other_investor.active_version.country_id}
                if other_investor.active_version
                else None,
                "classification": other_investor.active_version.classification,
                "deleted": other_investor.deleted,
            }
            if other_investor
            else None
        )

        return {
            "id": self.id,
            "other_investor": other_investor_dict,
            "relationship": relationship,
            "investment_type": self.investment_type,
            "percentage": self.percentage,
            "loans_amount": self.loans_amount,
            "loans_currency": self.loans_currency,
            "loans_date": self.loans_date,
            "parent_relation": self.parent_relation,
            "comment": self.comment,
        }
