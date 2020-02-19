import reversion
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.greennewdeal.models.country import Country
from apps.greennewdeal.models.mixins import (
    OldContractMixin,
    OldDataSourceMixin,
    OldDealMixin,
    OldLocationMixin,
    ReversionSaveMixin,
)


@reversion.register(
    follow=["locations", "contracts", "datasources"], ignore_duplicates=True
)
class Deal(models.Model, ReversionSaveMixin, OldDealMixin):
    """ Deal """

    """ Locations """
    # is a foreign key

    """ General info """
    # Land area
    target_country = models.ForeignKey(
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
    intention_of_investment = JSONField(
        _("Intention of the investment"), blank=True, null=True
    )
    intention_of_investment_comment = models.TextField(blank=True)

    # Nature of the deal
    NATURE_OF_DEAL_CHOICES = (
        (10, _("Outright Purchase")),
        (20, _("Lease")),
        (30, _("Concession")),
        (40, _("Exploitation permit / license / concession (for mineral resources)")),
        (50, _("Pure contract farming")),
    )
    nature_of_deal = ArrayField(
        models.IntegerField(_("Nature of the deal"), choices=NATURE_OF_DEAL_CHOICES),
        blank=True,
        null=True,
    )
    nature_of_deal_comment = models.TextField(
        _("Comment on nature of the deal"), blank=True
    )

    negotiation_status = JSONField(_("Negotiation status"), blank=True, null=True)
    negotiation_status_comment = models.TextField(
        _("Comment on negotiation status"), blank=True
    )

    # # Implementation status
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
        (10, _("per ha")),
        (20, _("for specified area")),
    )
    purchase_price_type = models.IntegerField(
        choices=HA_AREA_CHOICES, blank=True, null=True
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
    annual_leasing_fee_type = models.IntegerField(
        choices=HA_AREA_CHOICES, blank=True, null=True
    )
    annual_leasing_fee_area = models.DecimalField(
        _("Annual leasing fee area"),
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    annual_leasing_fees_comment = models.TextField(
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
        _("On leased / purchased farmers"), help_text=_("ha"), blank=True, null=True,
    )
    on_the_lease_households = JSONField(
        _("On leased / purchased households"), help_text=_("ha"), blank=True, null=True,
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
        help_text=_("ha"),
        blank=True,
        null=True,
    )
    off_the_lease_households = JSONField(
        _("Not on leased / purchased households (out-grower)"),
        help_text=_("ha"),
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
        "Investor",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deals",
    )
    involved_actors = JSONField(
        _("Actors involved in the negotiation / admission process"),
        blank=True,
        null=True,
    )
    project_name = models.CharField(max_length=255, blank=True)
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
            10,
            "Indigenous Peoples traditional or customary rights recognized by government",
        ),
        (
            20,
            "Indigenous Peoples traditional or customary rights not recognized by government",
        ),
        (30, "Community traditional or customary rights recognized by government"),
        (40, "Community traditional or customary rights not recognized by government"),
    )
    recognition_status = ArrayField(
        models.IntegerField(_("Name of community"), choices=RECOGNITION_STATUS_CHOICES),
        blank=True,
        null=True,
    )
    recognition_status_comment = models.TextField(
        _("Comment on recognitions status of community land tenure"), blank=True
    )
    COMMUNITY_CONSULTATION_CHOICES = (
        (10, "Not consulted"),
        (20, "Limited consultation"),
        (30, "Free, Prior and Informed Consent (FPIC)"),
        (40, "Certified Free, Prior and Informed Consent (FPIC)"),
        (50, "Other"),
    )
    community_consultation = models.IntegerField(
        _("Community consultation"),
        choices=COMMUNITY_CONSULTATION_CHOICES,
        blank=True,
        null=True,
    )
    community_consultation_comment = models.TextField(
        _("Comment on consultation of local community"), blank=True
    )

    COMMUNITY_REACTION_CHOICES = (
        (10, "Consent"),
        (20, "Mixed reaction"),
        (30, "Rejection"),
    )
    community_reaction = models.IntegerField(
        _("Community reaction"),
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
        (10, "Environmental degradation"),
        (20, "Socio-economic"),
        (30, "Cultural loss"),
        (40, "Eviction"),
        (50, "Displacement"),
        (60, "Violence"),
        (70, "Other"),
    )
    negative_impacts = ArrayField(
        models.IntegerField(
            _("Negative impacts for local communities"),
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
        (10, "Health"),
        (20, "Education"),
        (30, "Productive infrastructure (e.g. irrigation, tractors, machinery...)"),
        (40, "Roads"),
        (50, "Capacity Building"),
        (60, "Financial Support"),
        (70, "Community shares in the investment project"),
        (80, "Other"),
    )
    promised_benefits = ArrayField(
        models.IntegerField(
            _("Promised benefits for local communities"), choices=BENEFITS_CHOICES
        ),
        blank=True,
        null=True,
    )
    promised_benefits_comment = models.TextField(
        _("Comment on promised benefits for local communities"), blank=True
    )

    materialized_benefits = ArrayField(
        models.IntegerField(
            _("Promised benefits for local communities"), choices=BENEFITS_CHOICES
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
        (10, "State"),
        (20, "Private (smallholders)"),
        (30, "Private (large-scale farm)"),
        (40, "Community"),
        (50, "Indigenous people"),
        (60, "Other"),
    )
    former_land_owner = ArrayField(
        models.IntegerField(_("Former land owner"), choices=FORMER_LAND_OWNER_CHOICES),
        blank=True,
        null=True,
    )
    former_land_owner_comment = models.TextField(
        _("Comment on former land owner"), blank=True
    )

    FORMER_LAND_USE_CHOICES = (
        (10, "Commercial (large-scale) agriculture"),
        (20, "Smallholder agriculture"),
        (30, "Shifting cultivation"),
        (40, "Pastoralism"),
        (50, "Hunting/Gathering"),
        (60, "Forestry"),
        (70, "Conservation"),
        (80, "Other"),
    )

    former_land_use = ArrayField(
        models.IntegerField(_("Former land use"), choices=FORMER_LAND_USE_CHOICES),
        blank=True,
        null=True,
    )
    former_land_use_comment = models.TextField(
        _("Comment on former land use"), blank=True
    )

    FORMER_LAND_COVER_CHOICES = (
        (10, "Cropland"),
        (20, "Forest land"),
        (30, "Pasture"),
        (40, "Shrub land/Grassland (Rangeland)"),
        (50, "Marginal land"),
        (60, "Wetland"),
        (70, "Other land (e.g. developed land – specify in comment field)"),
    )

    former_land_cover = ArrayField(
        models.IntegerField(_("Former land cover"), choices=FORMER_LAND_COVER_CHOICES),
        blank=True,
        null=True,
    )
    former_land_cover_comment = models.TextField(
        _("Comment on former land cover"), blank=True
    )

    """ Produce info """
    crops = JSONField(_("Crops area"), help_text=_("ha"), blank=True, null=True)
    crops_yield = JSONField(
        _("Crops yield"), help_text=_("tons"), blank=True, null=True
    )
    crops_export = JSONField(_("Crops export"), help_text=_("%"), blank=True, null=True)
    crops_comment = models.TextField(blank=True)

    animals = JSONField(_("Livestock area"), help_text=_("ha"), blank=True, null=True)
    animals_yield = JSONField(
        _("Livestock yield"), help_text=_("tons"), blank=True, null=True
    )
    animals_export = JSONField(
        _("Livestock export"), help_text=_("%"), blank=True, null=True
    )
    animals_comment = models.TextField(blank=True)

    resources = JSONField(_("Resources area"), help_text=_("ha"), blank=True, null=True)
    resources_yield = JSONField(
        _("Resources yield"), help_text=_("tons"), blank=True, null=True
    )
    resources_export = JSONField(
        _("Resources export"), help_text=_("%"), blank=True, null=True
    )
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
        (10, "Groundwater"),
        (20, "Surface water"),
        (21, "River"),
        (22, "Lake"),
    )
    source_of_water_extraction = ArrayField(
        models.IntegerField(
            _("Source of water extraction"), choices=WATER_SOURCE_CHOICES
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
    YPN_CHOICES = ((1, "Yes"), (2, "Partially"), (3, "No"))

    vggt_applied = models.IntegerField(
        _(
            "Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)"
        ),
        choices=YPN_CHOICES,
        blank=True,
        null=True,
    )
    vggt_applied_comment = models.TextField(_("Comment on VGGT"), blank=True)

    prai_applied = models.IntegerField(
        _("Application of Principles for Responsible Agricultural Investments (PRAI)"),
        choices=YPN_CHOICES,
        blank=True,
        null=True,
    )
    prai_applied_comment = models.TextField(_("Comment on PRAI"), blank=True)

    """ Overall comment """
    overall_comment = models.TextField(_("Overall comment"), blank=True)

    # Meta info
    "fully_updated"
    "not_public"
    "not_public_reason"
    "tg_not_public_comment"
    "previous_identifier"
    "assign_to_user"
    "tg_feedback_comment"
    "terms"

    STATUS_CHOICES = [
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Live + Draft")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"#{self.id} in {self.target_country}"


@reversion.register(ignore_duplicates=True)
class Location(models.Model, OldLocationMixin):
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    point = gismodels.PointField(blank=True, null=True)
    facility_name = models.CharField(max_length=255, blank=True)
    ACCURACY_CHOICES = (
        (50, _("Country")),
        (40, _("Administrative region")),
        (30, _("Approximate location")),
        (20, _("Exact location")),
        (10, _("Coordinates")),
    )
    level_of_accuracy = models.IntegerField(
        choices=ACCURACY_CHOICES, blank=True, null=True
    )
    comment = models.TextField(blank=True)

    contract_area = gismodels.MultiPolygonField(blank=True, null=True)
    intended_area = gismodels.MultiPolygonField(blank=True, null=True)
    production_area = gismodels.MultiPolygonField(blank=True, null=True)

    deal = models.ForeignKey(Deal, on_delete=models.PROTECT, related_name="locations")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"(#{self.deal_id}) {self.name}"


@reversion.register(ignore_duplicates=True)
class Contract(models.Model, OldContractMixin):
    number = models.CharField(_("Contract number"), max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    agreement_duration = models.IntegerField(
        _("Duration of the agreement (in years)"), blank=True, null=True
    )
    comment = models.TextField(blank=True)

    deal = models.ForeignKey(Deal, on_delete=models.PROTECT, related_name="contracts")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"(#{self.deal_id}) {self.number}"


@reversion.register(ignore_duplicates=True)
class DataSource(models.Model, OldDataSourceMixin):
    TYPE_CHOICES = (
        (10, _("Media report")),
        (20, _("Research Paper / Policy Report")),
        (30, _("Government sources")),
        (40, _("Company sources")),
        (50, _("Contract")),
        (60, _("Contract (contract farming agreement)")),
        (70, _("Personal information")),
        (80, _("Crowdsourcing")),
        (90, _("Other (Please specify in comment field)")),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True)
    url = models.URLField(max_length=1000, blank=True, null=True)
    file = models.FileField(
        _("File"),
        upload_to="uploads",
        max_length=500,
        help_text=_("Maximum file size: 10MB"),
        blank=True,
        null=True,
    )
    file_not_public = models.BooleanField(_("Keep PDF not public"), default=False)
    publication_title = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=255, blank=True)
    company = models.CharField(_("Company"), max_length=255, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=255, blank=True)

    includes_in_country_verified_information = models.BooleanField(
        _("Includes in-country-verified information"), default=False
    )
    open_land_contracts_id = models.CharField(max_length=255, blank=True)
    comment = models.TextField(_("Comment on data source"), blank=True)

    deal = models.ForeignKey(Deal, on_delete=models.PROTECT, related_name="datasources")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"(#{self.deal_id}) {self.get_type_display()}"
