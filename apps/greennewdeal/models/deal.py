import json

import reversion
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.greennewdeal.models import Investor
from apps.greennewdeal.models.country import Country
from apps.greennewdeal.models.mixins import (
    OldDealMixin,
    ReversionSaveMixin,
    UnderscoreDisplayParseMixin,
)


class DealManager(models.Manager):
    def visible(self, user=None):
        qs = self.get_queryset()
        if user and (user.is_staff or user.is_superuser):
            return qs
        return qs.filter(status__in=(2, 3), confidential=False)

    def public(self):
        qs = self.get_queryset()
        qs = qs.exclude(confidential=True)
        qs = qs.exclude(country=None).exclude(country__high_income=True)
        qs = qs.exclude(datasources=None)
        qs = qs.exclude(operating_company=None)
        qs = qs.exclude(
            Q(operating_company__is_actually_unknown=True)
            & ~Q(operating_company__investors__investor__is_actually_unknown=False)
        )
        # TODO: Open question: just role = "Stakeholder"?
        return qs


@reversion.register(
    follow=("locations", "contracts", "datasources"), ignore_duplicates=True,
)
class Deal(models.Model, UnderscoreDisplayParseMixin, ReversionSaveMixin, OldDealMixin):
    """ Deal """

    """ Locations """
    # is a foreign key

    """ General info """
    # Land area
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True
    )
    intended_size = models.DecimalField(
        _("Intended size"), max_digits=12, decimal_places=2, blank=True, null=True
    )
    contract_size = JSONField(
        _("Size under contract (leased or purchased area, in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    production_size = JSONField(
        _("Size in operation (production, in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    land_area_comment = models.TextField(blank=True)

    # Intention of investment
    INTENTION_CHOICES = (
        # Agriculture
        ("BIOFUELS", "Biofuels"),
        ("FOOD_CROPS", "Food crops"),
        ("FODDER", "Fodder"),
        ("LIVESTOCK", "Livestock"),
        ("NON_FOOD_AGRICULTURE", "Non-food agricultural commodities"),
        ("AGRICULTURE_UNSPECIFIED", "Agriculture unspecified"),
        # Forestry
        ("TIMBER_PLANTATION", "Timber plantation"),
        ("FOREST_LOGGING", "Forest logging / management"),
        ("CARBON", "For carbon sequestration/REDD"),
        ("FORESTRY_UNSPECIFIED", "Forestry unspecified"),
        # Other
        ("MINING", "Mining"),
        ("OIL_GAS_EXTRACTION", "Oil / Gas extraction"),
        ("TOURISM", "Tourism"),
        ("INDUSTRY", "Industry"),
        ("CONVERSATION", "Conservation"),
        ("LAND_SPECULATION", "Land speculation"),
        ("RENEWABLE_ENERGY", "Renewable Energy"),
        ("OTHER", "Other"),
    )
    intention_of_investment = JSONField(
        _("Intention of the investment"), blank=True, null=True
    )
    intention_of_investment_comment = models.TextField(blank=True)

    # Nature of the deal
    NATURE_OF_DEAL_CHOICES = (
        ("OUTRIGHT_PURCHASE", _("Outright Purchase")),
        ("LEASE", _("Lease")),
        ("CONCESSION", _("Concession")),
        (
            "EXPLOITATION_PERMIT",
            _("Exploitation permit / license / concession (for mineral resources)"),
        ),
        ("PURE_CONTRACT_FARMING", _("Pure contract farming")),
    )
    nature_of_deal = ArrayField(
        models.CharField(
            _("Nature of the deal"), max_length=100, choices=NATURE_OF_DEAL_CHOICES
        ),
        blank=True,
        null=True,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"), blank=True
    )

    # # Negotiation status
    NEGOTIATION_STATUS_CHOICES = (
        ("EXPRESSION_OF_INTEREST", "Expression of interest"),
        ("UNDER_NEGOTIATION", "Under negotiation"),
        ("MEMORANDUM_OF_UNDERSTANDING", "Memorandum of understanding"),
        ("ORAL_AGREEMENT", "Oral agreement"),
        ("CONTRACT_SIGNED", "Contract signed"),
        ("NEGOTIATIONS_FAILED", "Negotiations failed"),
        ("CONTRACT_CANCELED", "Contract canceled"),
        ("CONTRACT_EXPIRED", "Contract expired"),
        ("CHANGE_OF_OWNERSHIP", "Change of ownership"),
    )
    negotiation_status = JSONField(_("Negotiation status"), blank=True, null=True)
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
    implementation_status = JSONField(_("Implementation status"), blank=True, null=True)
    implementation_status_comment = models.TextField(
        _("Comment on implementation status"), blank=True
    )

    # Purchase price
    purchase_price = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    purchase_price_currency = models.ForeignKey(
        "Currency",
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
        max_length=100, choices=HA_AREA_CHOICES, blank=True, null=True
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
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    annual_leasing_fee_currency = models.ForeignKey(
        "Currency",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deal_annual_leasing_fee",
    )
    annual_leasing_fee_type = models.CharField(
        max_length=100, choices=HA_AREA_CHOICES, blank=True, null=True
    )
    annual_leasing_fee_area = models.DecimalField(
        _("Annual leasing fee area"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    annual_leasing_fee_comment = models.TextField(
        _("Comment on leasing fees"), blank=True
    )

    # Contract farming
    contract_farming = models.BooleanField(default=False)

    on_the_lease = models.BooleanField(_("On leased / purchased area"), default=False)
    on_the_lease_area = JSONField(
        _("On leased / purchased area (in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    on_the_lease_farmers = JSONField(
        _("On leased / purchased farmers"),
        help_text=_("farmers"),
        blank=True,
        null=True,
    )
    on_the_lease_households = JSONField(
        _("On leased / purchased households"),
        help_text=_("households"),
        blank=True,
        null=True,
    )

    off_the_lease = models.BooleanField(
        _("Not on leased / purchased area (out-grower)"), default=False
    )
    off_the_lease_area = JSONField(
        _("Not on leased / purchased area (out-grower, in ha)"),
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    off_the_lease_farmers = JSONField(
        _("Not on leased / purchased farmers (out-grower)"),
        help_text=_("farmers"),
        blank=True,
        null=True,
    )
    off_the_lease_households = JSONField(
        _("Not on leased / purchased households (out-grower)"),
        help_text=_("households"),
        blank=True,
        null=True,
    )

    contract_farming_comment = models.TextField(
        _("Comment on contract farming"), blank=True
    )

    """ Contracts """
    # is a foreign key

    """ Employment """
    total_jobs_created = models.BooleanField(_("Jobs created (total)"), default=False)
    total_jobs_planned = models.IntegerField(
        _("Planned number of jobs (total)"), help_text=_("jobs"), blank=True, null=True
    )
    total_jobs_planned_employees = models.IntegerField(
        _("Planned employees (total)"), help_text=_("employees"), blank=True, null=True
    )
    total_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (total)"),
        help_text=_("workers"),
        blank=True,
        null=True,
    )
    total_jobs_current = JSONField(
        _("Current number of jobs (total)"), help_text=_("jobs"), blank=True, null=True,
    )
    total_jobs_current_employees = JSONField(
        _("Current number of employees (total)"),
        help_text=_("employees"),
        blank=True,
        null=True,
    )
    total_jobs_current_daily_workers = JSONField(
        _("Current number of daily/seasonal workers (total)"),
        help_text=_("workers"),
        blank=True,
        null=True,
    )
    total_jobs_created_comment = models.TextField(
        _("Comment on jobs created (total)"), blank=True
    )

    # TODO: should this be NullBoolean? same goes for many other fields.
    foreign_jobs_created = models.BooleanField(
        _("Jobs created (foreign)"), default=False
    )
    foreign_jobs_planned = models.IntegerField(
        _("Planned number of jobs (foreign)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
    )
    foreign_jobs_planned_employees = models.IntegerField(
        _("Planned employees (foreign)"),
        help_text=_("employees"),
        blank=True,
        null=True,
    )
    foreign_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (foreign)"),
        help_text=_("workers"),
        blank=True,
        null=True,
    )
    foreign_jobs_current = JSONField(
        _("Current number of jobs (foreign)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
    )
    foreign_jobs_current_employees = JSONField(
        _("Current number of employees (foreign)"),
        help_text=_("employees"),
        blank=True,
        null=True,
    )
    foreign_jobs_current_daily_workers = JSONField(
        _("Current number of daily/seasonal workers (foreign)"),
        help_text=_("workers"),
        blank=True,
        null=True,
    )
    foreign_jobs_created_comment = models.TextField(
        _("Comment on jobs created (foreign)"), blank=True
    )

    domestic_jobs_created = models.BooleanField(
        _("Jobs created (domestic)"), default=False
    )
    domestic_jobs_planned = models.IntegerField(
        _("Planned number of jobs (domestic)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
    )
    domestic_jobs_planned_employees = models.IntegerField(
        _("Planned employees (domestic)"),
        help_text=_("employees"),
        blank=True,
        null=True,
    )
    domestic_jobs_planned_daily_workers = models.IntegerField(
        _("Planned daily/seasonal workers (domestic)"),
        help_text=_("workers"),
        blank=True,
        null=True,
    )
    domestic_jobs_current = JSONField(
        _("Current number of jobs (domestic)"),
        help_text=_("jobs"),
        blank=True,
        null=True,
    )
    domestic_jobs_current_employees = JSONField(
        _("Current number of employees (domestic)"),
        help_text=_("employees"),
        blank=True,
        null=True,
    )
    domestic_jobs_current_daily_workers = JSONField(
        _("Current number of daily/seasonal workers (domestic)"),
        help_text=_("workers"),
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
                "Government / State institutions (government, ministries, departments, agencies etc.)"
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
    involved_actors = JSONField(
        _("Actors involved in the negotiation / admission process"),
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
    # is a foreign key

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
            "Indigenous Peoples traditional or customary rights recognized by government",
        ),
        (
            "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
            "Indigenous Peoples traditional or customary rights not recognized by government",
        ),
        (
            "COMMUNITY_RIGHTS_RECOGNIZED",
            "Community traditional or customary rights recognized by government",
        ),
        (
            "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
            "Community traditional or customary rights not recognized by government",
        ),
    )
    recognition_status = ArrayField(
        models.CharField(
            _("Recognition status"), max_length=100, choices=RECOGNITION_STATUS_CHOICES
        ),
        blank=True,
        null=True,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognitions status of community land tenure"), blank=True
    )
    COMMUNITY_CONSULTATION_CHOICES = (
        ("NOT_CONSULTED", "Not consulted"),
        ("LIMITED_CONSULTATION", "Limited consultation"),
        ("FPIC", "Free, Prior and Informed Consent (FPIC)"),
        ("OTHER", "Other"),
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
        ("CONSENT", "Consent"),
        ("MIXED_REACTION", "Mixed reaction"),
        ("REJECTION", "Rejection"),
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

    land_conflicts = models.NullBooleanField(_("Presence of land conflicts"))
    land_conflicts_comment = models.TextField(
        _("Comment on presence of land conflicts"), blank=True
    )

    displacement_of_people = models.NullBooleanField(_("Displacement of people"))
    displaced_people = models.IntegerField(
        _("Number of people actually displaced"), blank=True, null=True
    )  # number_of_displaced_people
    displaced_households = models.IntegerField(
        _("Number of households actually displaced"), blank=True, null=True
    )  # number_of_displaced_households
    displaced_people_from_community_land = models.IntegerField(
        _("Number of people displaced out of their community land"),
        blank=True,
        null=True,
    )  # number_of_people_displaced_from_community_land
    displaced_people_within_community_land = models.IntegerField(
        _("Number of people displaced staying on community land"), blank=True, null=True
    )  # number_of_people_displaced_within_community_land
    displaced_households_from_fields = models.IntegerField(
        _('Number of households displaced "only" from their agricultural fields'),
        blank=True,
        null=True,
    )  # number_of_households_displaced_from_fields
    displaced_people_on_completion = models.IntegerField(
        _("Number of people facing displacement once project is fully implemented"),
        blank=True,
        null=True,
    )  # number_of_people_displaced_on_completion
    displacement_of_people_comment = models.TextField(
        _("Comment on presence of land conflicts"), blank=True
    )

    NEGATIVE_IMPACTS_CHOICES = (
        ("ENVIRONMENTAL_DEGRADATION", "Environmental degradation"),
        ("SOCIO_ECONOMIC", "Socio-economic"),
        ("CULTURAL_LOSS", "Cultural loss"),
        ("EVICTION", "Eviction"),
        ("DISPLACEMENT", "Displacement"),
        ("VIOLENCE", "Violence"),
        ("OTHER", "Other"),
    )
    negative_impacts = ArrayField(
        models.CharField(
            _("Negative impacts for local communities"),
            max_length=100,
            choices=NEGATIVE_IMPACTS_CHOICES,
        ),
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
        ("HEALTH", "Health"),
        ("EDUCATION", "Education"),
        (
            "PRODUCTIVE_INFRASTRUCTURE",
            "Productive infrastructure (e.g. irrigation, tractors, machinery...)",
        ),
        ("ROADS", "Roads"),
        ("CAPACITY_BUILDING", "Capacity Building"),
        ("FINANCIAL_SUPPORT", "Financial Support"),
        ("COMMUNITY_SHARES", "Community shares in the investment project"),
        ("OTHER", "Other"),
    )
    promised_benefits = ArrayField(
        models.CharField(
            _("Promised benefits for local communities"),
            max_length=100,
            choices=BENEFITS_CHOICES,
        ),
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
            choices=BENEFITS_CHOICES,
        ),
        blank=True,
        null=True,
    )
    materialized_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    presence_of_organizations = models.TextField(
        _(
            "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"
        ),
        blank=True,
    )

    """ Former use """
    FORMER_LAND_OWNER_CHOICES = (
        ("STATE", "State"),
        ("PRIVATE_SMALLHOLDERS", "Private (smallholders)"),
        ("PRIVATE_LARGE_SCALE", "Private (large-scale farm)"),
        ("COMMUNITY", "Community"),
        ("INDIGENOUS_PEOPLE", "Indigenous people"),
        ("OTHER", "Other"),
    )
    former_land_owner = ArrayField(
        models.CharField(
            _("Former land owner"), max_length=100, choices=FORMER_LAND_OWNER_CHOICES
        ),
        blank=True,
        null=True,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )

    FORMER_LAND_USE_CHOICES = (
        ("COMMERCIAL_AGRICULTURE", "Commercial (large-scale) agriculture"),
        ("SMALLHOLDER_AGRICULTURE", "Smallholder agriculture"),
        ("SHIFTING_CULTIVATION", "Shifting cultivation"),
        ("PASTORALISM", "Pastoralism"),
        ("HUNTING_GATHERING", "Hunting/Gathering"),
        ("FORESTRY", "Forestry"),
        ("CONSERVATION", "Conservation"),
        ("OTHER", "Other"),
    )

    former_land_use = ArrayField(
        models.CharField(
            _("Former land use"), max_length=100, choices=FORMER_LAND_USE_CHOICES
        ),
        blank=True,
        null=True,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )

    FORMER_LAND_COVER_CHOICES = (
        ("CROPLAND", "Cropland"),
        ("FOREST_LAND", "Forest land"),
        ("PASTURE", "Pasture"),
        ("RANGELAND", "Shrub land/Grassland (Rangeland)"),
        ("MARGINAL_LAND", "Marginal land"),
        ("WETLAND", "Wetland"),
        ("OTHER_LAND", "Other land (e.g. developed land – specify in comment field)"),
    )

    former_land_cover = ArrayField(
        models.CharField(
            _("Former land cover"), max_length=100, choices=FORMER_LAND_COVER_CHOICES
        ),
        blank=True,
        null=True,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"), blank=True
    )

    """ Produce info """
    crops = JSONField(_("Crops"), blank=True, null=True)
    crops_comment = models.TextField(blank=True)

    animals = JSONField(_("Livestock"), blank=True, null=True)
    animals_comment = models.TextField(blank=True)

    resources = JSONField(_("Resources"), blank=True, null=True)
    resources_comment = models.TextField(blank=True)

    contract_farming_crops = JSONField(
        _("Contract farming crops"), help_text=_("ha"), blank=True, null=True
    )
    contract_farming_crops_comment = models.TextField(
        _("Comment on contract farming crops"), blank=True
    )
    contract_farming_animals = JSONField(
        _("Contract farming livestock"), help_text=_("ha"), blank=True, null=True
    )
    contract_farming_animals_comment = models.TextField(
        _("Comment on contract farming livestock"), blank=True
    )

    has_domestic_use = models.BooleanField(_("Has domestic use"), default=False)
    domestic_use = models.FloatField(
        _("Ownership share"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    has_export = models.BooleanField(_("Has export"), default=False)

    export_country1 = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    export_country1_ratio = models.FloatField(
        _("Country 1 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country2 = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    export_country2_ratio = models.FloatField(
        _("Country 2 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    export_country3 = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    export_country3_ratio = models.FloatField(
        _("Country 3 ratio"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    use_of_produce_comment = models.TextField(blank=True)

    in_country_processing = models.NullBooleanField(
        _("In country processing of produce")
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
    water_extraction_envisaged = models.NullBooleanField(
        _("Water extraction envisaged")
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
        models.CharField(
            _("Source of water extraction"),
            max_length=100,
            choices=WATER_SOURCE_CHOICES,
        ),
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
    use_of_irrigation_infrastructure = models.NullBooleanField(
        _("Use of irrigation infrastructure")
    )
    use_of_irrigation_infrastructure_comment = models.TextField(
        _("Comment on use of irrigation infrastructure"), blank=True
    )
    water_footprint = models.TextField(
        _("Water footprint of the investment project"), blank=True
    )

    """ Gender-related info """
    gender_related_information = models.TextField(
        _("Gender-related information"), blank=True
    )

    """ Guidelines & Principles """
    YPN_CHOICES = (("YES", "Yes"), ("PARTIALLY", "Partially"), ("NO", "No"))

    vggt_applied = models.CharField(
        _(
            "Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)"
        ),
        max_length=100,
        choices=YPN_CHOICES,
        blank=True,
        null=True,
    )
    vggt_applied_comment = models.TextField(_("Comment on VGGT"), blank=True)

    prai_applied = models.CharField(
        _("Application of Principles for Responsible Agricultural Investments (PRAI)"),
        max_length=100,
        choices=YPN_CHOICES,
        blank=True,
        null=True,
    )
    prai_applied_comment = models.TextField(_("Comment on PRAI"), blank=True)

    """ Overall comment """
    overall_comment = models.TextField(_("Overall comment"), blank=True)

    """ Meta Info """
    fully_updated = models.BooleanField(default=False)
    confidential = models.BooleanField(default=False)
    PRIVATE_REASON_CHOICES = (
        ("TEMPORARY_REMOVAL", "Temporary removal from PI after criticism"),
        ("RESEARCH_IN_PROGRESS", "Research in progress"),
        ("LAND_OBSERVATORY_IMPORT", "Land Observatory Import"),
    )
    confidential_reason = models.CharField(
        max_length=100, choices=PRIVATE_REASON_CHOICES, null=True, blank=True
    )
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True
    )

    # Meta info
    "previous_identifier"
    "assign_to_user"
    "tg_feedback_comment"
    "terms"

    """ # CALCULATED FIELDS # """
    deal_size = models.IntegerField(blank=True, null=True)
    current_negotiation_status = models.CharField(
        choices=NEGOTIATION_STATUS_CHOICES, max_length=100, blank=True, null=True
    )
    current_implementation_status = models.CharField(
        choices=IMPLEMENTATION_STATUS_CHOICES, max_length=100, blank=True, null=True
    )
    current_contract_size = models.FloatField(blank=True, null=True)
    current_production_size = models.FloatField(blank=True, null=True)
    geojson = JSONField(blank=True, null=True)

    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Updated")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    )
    DRAFT_STATUS_CHOICES = (
        (1, "Draft"),
        (2, "Review"),
        (3, "Activation"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    objects = DealManager()

    def __str__(self):
        return f"#{self.id} in {self.country}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.current_contract_size = self._get_current("contract_size")
        self.current_production_size = self._get_current("production_size")
        self.current_negotiation_status = self._get_current("negotiation_status")
        self.current_implementation_status = self._get_current("implementation_status")
        self.deal_size = self._calculate_deal_size()
        self.geojson = self._combine_geojson()
        super(Deal, self).save(*args, **kwargs)

    def _get_current(self, attribute):
        attributes: list = self.__getattribute__(attribute)
        if not attributes:
            return None
        # prioritize "current" checkbox if present
        current = [x for x in attributes if x.get("current")]
        if current:
            return current[0].get("value")
        # last given entry, if no it has no date
        most_recent = attributes[-1]
        if not most_recent.get("date"):
            return most_recent.get("value")
        # most recent year/date given
        most_recent = sorted(
            [a for a in attributes if a.get("date")],
            key=lambda x: x.get("date"),
            reverse=True,
        )[0]
        return most_recent.get("value")

    def _calculate_deal_size(self):
        negotiation_status = self.current_negotiation_status
        if not negotiation_status:
            return 0

        intended_size = int(self.intended_size or 0)
        contract_size = int(self.current_contract_size or 0)
        production_size = int(self.current_production_size or 0)

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
            value = 0
        return value

    # def _calculate_init_date(self):
    #     init_dates = []
    #     self.negotiation_status
    #     negotiation_stati = self.attributes.filter(
    #         name="negotiation_status",
    #         value__in=(
    #             # NEGOTIATION_STATUS_EXPRESSION_OF_INTEREST, - removed, see #1154
    #             self.NEGOTIATION_STATUS_UNDER_NEGOTIATION,
    #             self.NEGOTIATION_STATUS_ORAL_AGREEMENT,
    #             self.NEGOTIATION_STATUS_CONTRACT_SIGNED,
    #             self.NEGOTIATION_STATUS_NEGOTIATIONS_FAILED,
    #             self.NEGOTIATION_STATUS_CONTRACT_CANCELLED,
    #         ),
    #     ).order_by("date")
    #     implementation_stati = self.attributes.filter(
    #         name="implementation_status",
    #         value__in=(
    #             self.IMPLEMENTATION_STATUS_STARTUP_PHASE,
    #             self.IMPLEMENTATION_STATUS_IN_OPERATION,
    #             self.IMPLEMENTATION_STATUS_PROJECT_ABANDONED,
    #         ),
    #     ).order_by("date")
    #     if negotiation_stati.count() > 0:
    #         if negotiation_stati[0].date:
    #             init_dates.append(negotiation_stati[0].date)
    #     if implementation_stati.count() > 0:
    #         if implementation_stati[0].date:
    #             init_dates.append(implementation_stati[0].date)
    #     if init_dates:
    #         return min(init_dates)

    def _combine_geojson(self):
        features = []
        for loc in self.locations.all():  # type: Location
            if loc.point:
                point = {
                    "type": "Feature",
                    "geometry": (json.loads(loc.point.geojson)),
                    "properties": {"name": loc.name, "id": loc.id, "type": "point"},
                }
                features += [point]
            if loc.areas:
                feats = loc.areas["features"]
                for feat in feats:
                    feat["properties"]["name"] = loc.name
                    feat["properties"]["id"] = loc.id
                    features += [feat]
        if not features:
            return None
        return {"type": "FeatureCollection", "features": features}

    @property
    def top_investors(self):
        """
        Get list of highest parent companies
        (all right-hand side parent companies of the network visualisation)
        """
        if self.operating_company:
            return self.operating_company.get_top_investors()

    class IsNotPublic(Exception):
        pass

    def is_public_deal(self):
        # 1. Flag "confidential"
        if self.confidential:
            raise self.IsNotPublic("Confidential Flag")
        # 2. Minimum information missing?
        # No Country or High Income Country?
        if not self.country or self.country.high_income:
            raise self.IsNotPublic("No Country or High-Income Country")
        # No DataSource?
        if not self.datasources.exists():
            raise self.IsNotPublic("No Datasources")
        # 3. No operating company?
        if not self.operating_company:
            raise self.IsNotPublic("No Operating Company")
        # 4A. Unknown operating company AND no known operating company parents
        oc_has_no_known_parents = not (
            self.operating_company.investors.filter(
                investor__is_actually_unknown=False
            ).exists()
        )
        if self.operating_company.is_actually_unknown and oc_has_no_known_parents:
            raise self.IsNotPublic("No known investor")
        return True

    # def get_value_from_datevalueobject(self, name: str) -> Optional[str]:
    #     attribute = self.__getattribute__(name)
    #     if attribute:
    #         return attribute[0]["value"]
    #     return None
