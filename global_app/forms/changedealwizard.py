from django.utils.translation import ugettext_lazy as _
from django import forms

from global_app.forms import *

class ChangeDealSpatialFormSet(AddDealSpatialFormSet):
    extra = 0

class ChangeDealGeneralForm(BaseForm):
    # Old reliability ranking
    tg_reliability_ranking  = TitleField(required=False, label="", initial=_("Reliability ranking"))
    old_reliability_ranking = forms.CharField(required=False, label=_("Old reliability ranking"), widget=forms.TextInput(attrs={"readonly": "readonly"}))
    # Land area
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(required=False, label=_("Intended size"), help_text=_("ha"), widget=NumberInput)
    contract_size = forms.IntegerField(required=False, label=_("Current size under contract (leased or purchased area)"), help_text=_("ha"), widget=NumberInput)
    production_size = forms.IntegerField(required=False, label=_("Current size in operation (production)"), help_text=_("ha"), widget=NumberInput)
    tg_land_area_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Intention of investment
    tg_intention = TitleField(required=False, label="", initial=_("Intention of investment"))
    intention = NestedMultipleChoiceField(required=False, label=_("Intention of the investment"), choices=(
        (10, _("Agriculture"), (
           (11, _("Biofuels")),
           (12, _("Food crops")),
           (13, _("Livestock")),
           (14, _("Non-food agricultural commodities")),
           (15, _("Agriunspecified")),
        )),
        (20, _("Forestry"), (
           (21, _("For wood and fibre")),
           (22, _("For carbon sequestration/REDD")),
           (23, _("Forestunspecified")),
        )),
        (30, _("Mining"), None),
        (40, _("Tourism"), None),
        (60, _("Industry"), None),
        (70, _("Conservation"), None),
        (80, _("Renewable Energy"), None),
        (90, _("Other (please specify)"), None),
    ))
    tg_intention_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Nature of the deal
    tg_nature = TitleField(required=False, label="", initial=_("Nature of the deal"))
    nature = forms.MultipleChoiceField(required=False, label=_("Nature of the deal"), choices=(
        (10, _("Outright Purchase")),
        (20, _("Lease / Concession")),
        (30, _("Exploitation license")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_nature_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Negotiation status,
    tg_negotiation_status = TitleField(required=False, label="", initial=_("Negotiation status"))
    negotiation_status = YearBasedChoiceField(required=False, label=_("Negotiation status"), choices=(
        (0, _("---------")),
        (10, _("Intended (Expression of interest)")),
        (20, _("Intended (Under negotiation)")),
        (30, _("Concluded (Oral Agreement)")),
        (40, _("Concluded (Contract signed)")),
        (50, _("Failed (Negotiations failed)")),
        (60, _("Failed (Contract canceled)")),
    ))
    contract_number = forms.IntegerField(required=False, label=_("Contract number"));
    contract_date = forms.DateField(required=False, label=_("Contract date"), help_text="[dd:mm:yyyy]", input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"])
    tg_negotiation_status_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Duration of the agreement
    tg_agreement_duration = TitleField(required=False, label="", initial=_("Duration of the agreement"))
    agreement_duration = YearBasedIntegerField(required=False, label=_("Duration of the agreement"), help_text=_("years"))
    # Implementation status
    tg_implementation_status = TitleField(required=False, label="", initial=_("Implementation status"))
    implementation_status = YearBasedChoiceField(required=False, label=_("Implementation status"), choices=(
        (0, _("---------")),
        (10, _("Project not started")),
        (20, _("Startup phase (no production)")),
        (30, _("In operation (production)")),
        (40, _("Project abandoned")),
    ))
    tg_implementation_status_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Purchase price
    tg_purchase_price = TitleField(required=False, label="", initial=_("Purchase price"))
    purchase_price = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Purchase price"))
    purchase_price_currency = forms.ModelChoiceField(required=False, label=_("Purchase price currency"), queryset=Currency.objects.all().order_by("ranking", "name"))
    purchase_price_type = forms.TypedChoiceField(required=False, label=_("Purchase price area type"), choices=(
        (0, _("---------")),
        (10, _("per ha")),
        (20, _("for specified area")),
    ), coerce=int)
    purchase_price_area = forms.IntegerField(required=False, label=_("Purchase price area"), help_text=_("ha"), widget=NumberInput)
    tg_purchase_price_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Leasing fees
    tg_leasing_fees = TitleField(required=False, label="", initial=_("Leasing fees"))
    annual_leasing_fee = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Annual leasing fee"))
    annual_leasing_fee_currency = forms.ModelChoiceField(required=False, label=_("Annual leasing fee currency"), queryset=Currency.objects.all().order_by("ranking", "name"))
    annual_leasing_fee_type = forms.TypedChoiceField(required=False, label=_("Annual leasing fee type"), choices=(
        (0, _("---------")),
        (10, _("per ha")),
        (20, _("for specified area")),
    ), coerce=int)
    annual_leasing_fee_area = forms.IntegerField(required=False, label=_("Purchase price area"), help_text=_("ha"), widget=NumberInput)
    tg_leasing_fees_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Contract farming
    tg_contract_farming = TitleField(required=False, label="", initial=_("Contract farming"))
    contract_farming = forms.ChoiceField(required=False, label=_("Contract farming"), choices=(
        (10, _("Yes")),
        (20, _("No")),
    ), widget=forms.RadioSelect)
    on_the_lease = forms.BooleanField(required=False, label=_("On the lease"))
    on_the_lease_area = forms.IntegerField(required=False, label=_("On leased / purchased area"), help_text=_("ha"), widget=NumberInput)
    on_the_lease_farmers = forms.IntegerField(required=False, label=_("On leased / purchased farmers"), help_text=_("farmers"), widget=NumberInput)
    off_the_lease = forms.BooleanField(required=False, label=_("Not on the lease"))
    off_the_lease_area = forms.IntegerField(required=False, label=_("Not on leased / purchased area (out-grower)"), help_text=_("ha"), widget=NumberInput)
    off_the_lease_farmers = forms.IntegerField(required=False, label=_("Not on leased / purchased farmers (out-grower)"), help_text=_("farmers"), widget=NumberInput)
    tg_contract_farming_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def clean_contract_date(self):
        date = self.cleaned_data["contract_date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(_("Invalid date. Please enter a date in the format [dd:mm:yyyy]"))

class ChangeDealEmploymentForm(BaseForm): #FIXME super class adddealempl?
    # Total number of jobs created
    tg_total_number_of_jobs_created = TitleField(required=False, label="", initial=_("Number of total jobs created"))
    total_jobs_created = forms.BooleanField(required=False, label=_("Total number of jobs created"))
    total_jobs_planned = forms.IntegerField(required=False, label=_("Planned total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    total_jobs_current = YearBasedIntegerField(required=False, label=_("Current total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Current total employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    tg_total_number_of_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # Number of jobs for foreigners created
    tg_foreign_jobs_created = TitleField(required=False, label="", initial=_("Number of jobs for foreigners created"))
    foreign_jobs_created = forms.BooleanField(required=False, label=_("Number of jobs for foreigners created"))
    foreign_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of jobs for foreigners"), help_text=_("jobs"), widget=NumberInput)
    foreign_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    foreign_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    foreign_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of jobs for foreigners"), help_text=_("jobs"))
    foreign_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    foreign_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_foreign_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # Number of domestic jobs created
    tg_domestic_jobs_created = TitleField(required=False, label="", initial=_("Number of domestic jobs created"))
    domestic_jobs_created = forms.BooleanField(required=False, label=_("Number of domestic jobs created"))
    domestic_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of domestic jobs"), help_text=_("jobs"), widget=NumberInput)
    domestic_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    domestic_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    domestic_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of domestic jobs"), help_text=_("jobs"))
    domestic_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    domestic_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_domestic_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class ChangeDealDataSourceFormSet(AddDealDataSourceFormSet):
    extra = 0

class ChangeDealActionCommentForm(AddDealActionCommentForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=True, label="", widget=CommentInput)


class ChangeDealOverallCommentForm(BaseForm):
    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(required=False, label="", widget=CommentInput)

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        data = super(ChangeDealOverallCommentForm, cls).get_data(object, tg, prefix)
        comments = Comment.objects.filter(fk_a_tag_group__fk_activity=object.id, fk_a_tag_group__fk_a_tag__fk_a_value__value="overall").order_by("-timestamp")
        if comments and len(comments) > 0:
            data["tg_overall_comment"] = comments[0].comment
        return data

class ChangeInvestorForm(AddInvestorForm):

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        data = super(ChangeInvestorForm, cls).get_data(object, tg, prefix)
        return data
