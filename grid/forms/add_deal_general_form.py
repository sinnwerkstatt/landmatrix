__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import TitleField, CommentInput, NumberInput, NestedMultipleChoiceField, YearBasedChoiceField, \
    YearBasedIntegerField
from landmatrix.models.currency import Currency

from django import forms
from django.utils.translation import ugettext_lazy as _


class AddDealGeneralForm(BaseForm):

    form_title = _('General Info')

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
        (30, _("Concluded (Oral Agreement)")),
        (40, _("Concluded (Contract signed)")),
        (10, _("Intended (Expression of interest)")),
        (20, _("Intended (Under negotiation)")),
        (50, _("Failed (Negotiations failed)")),
        (60, _("Failed (Contract canceled)")),
    ))
    contract_number = forms.IntegerField(required=False, label=_("Contract number"))
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
    on_the_lease = forms.BooleanField(required=False, label=_("On leased / purchased area"))
    on_the_lease_area = forms.IntegerField(required=False, label=_("On leased / purchased area"), help_text=_("ha"), widget=NumberInput)
    on_the_lease_farmers = forms.IntegerField(required=False, label=_("On leased / purchased farmers"), help_text=_("farmers"), widget=NumberInput)
    off_the_lease = forms.BooleanField(required=False, label=_("Not on leased / purchased area (out-grower)"))
    off_the_lease_area = forms.IntegerField(required=False, label=_("Not on leased / purchased area (out-grower)"), help_text=_("ha"), widget=NumberInput)
    off_the_lease_farmers = forms.IntegerField(required=False, label=_("Not on leased / purchased farmers (out-grower)"), help_text=_("farmers"), widget=NumberInput)
    tg_contract_farming_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def clean_contract_date(self):
        date = self.cleaned_data["contract_date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(_("Invalid date. Please enter a date in the format [dd:mm:yyyy]"))

