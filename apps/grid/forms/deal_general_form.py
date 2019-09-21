from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.grid.fields import (TitleField, YearBasedChoiceField, YearBasedFloatField, YearBasedIntegerField, YearBasedMultipleChoiceIntegerField)
from apps.grid.widgets import CommentInput
from apps.landmatrix.models.activity import Activity
from apps.landmatrix.models import Currency
from .base_form import BaseForm
from .choices import grouped_intention_choices, nature_choices, price_type_choices


class DealGeneralForm(BaseForm):
    # TODO: why not boolean here? Maybe because there are three options: Yes, No or Unknown.
    CONTRACT_FARMING_CHOICES = (
        ("Yes", _("Yes")),
        ("No", _("No")),
    )

    form_title = _('General info')

    # Land area
    tg_land_area = TitleField(
        required=False, label="", initial=_("Land area"))
    intended_size = forms.FloatField(localize=True,
        required=False, label=_("Intended size (in ha)"), help_text=_("ha"),
        widget=forms.TextInput(attrs={'placeholder': _('Size'), 'class': 'form-control input-filter-number'}))
    contract_size = YearBasedFloatField(
        required=False,
        label=_("Size under contract (leased or purchased area, in ha)"),
        help_text=_("ha"), placeholder=_('Size'))
    production_size = YearBasedFloatField(
        required=False, label=_("Size in operation (production, in ha)"),
        help_text=_("ha"), placeholder=_('Size'))
    tg_land_area_comment = forms.CharField(
        required=False, label=_("Comment on land area"), widget=CommentInput)

    # Intention of investment
    tg_intention = TitleField(
        required=False, label="", initial=_("Intention of investment"))
    intention = YearBasedMultipleChoiceIntegerField(
        required=False, label=_("Intention of the investment"),
        choices=grouped_intention_choices)
    tg_intention_comment = forms.CharField(
        required=False, label=_("Comment on intention of investment"),
        widget=CommentInput)

    # Nature of the deal
    tg_nature = TitleField(
        required=False, label="", initial=_("Nature of the deal"))
    nature = forms.MultipleChoiceField(
        required=False, label=_("Nature of the deal"), choices=nature_choices,
        widget=forms.CheckboxSelectMultiple)
    tg_nature_comment = forms.CharField(
        required=False, label=_("Comment on nature of the deal"),
        widget=CommentInput)

    # Negotiation status,
    tg_negotiation_status = TitleField(
        required=False, label="", initial=_("Negotiation status")
    )
    negotiation_status = YearBasedChoiceField(
        required=False, label=_("Negotiation status"),
        choices=Activity.NEGOTIATION_STATUS_CHOICES)
    tg_negotiation_status_comment = forms.CharField(
        required=False, label=_("Comment on negotiation status"),
        widget=CommentInput)

    # Implementation status
    tg_implementation_status = TitleField(
        required=False, label="", initial=_("Implementation status"))
    implementation_status = YearBasedChoiceField(
        required=False, label=_("Implementation status"),
        choices=Activity.IMPLEMENTATION_STATUS_CHOICES)
    tg_implementation_status_comment = forms.CharField(
        required=False, label=_("Comment on implementation status"),
        widget=CommentInput)

    # Purchase price
    tg_purchase_price = TitleField(
        required=False, label="", initial=_("Purchase price"))
    purchase_price = forms.DecimalField(
        max_digits=19, decimal_places=2, required=False,
        label=_("Purchase price"))
    purchase_price_currency = forms.ModelChoiceField(
        required=False, label=_("Purchase price currency"),
        queryset=Currency.objects.all().order_by("ranking", "name"))
    purchase_price_type = forms.TypedChoiceField(
        required=False, label=_("Purchase price area type"),
        choices=price_type_choices)
    purchase_price_area = forms.IntegerField(
        required=False, label=_("Purchase price area"), help_text=_("ha"),
        widget=forms.NumberInput(attrs={'placeholder': _('Size')}))
    tg_purchase_price_comment = forms.CharField(
        required=False, label=_("Comment on purchase price"),
        widget=CommentInput)

    # Leasing fees
    tg_leasing_fees = TitleField(
        required=False, label="", initial=_("Leasing fees"))
    annual_leasing_fee = forms.DecimalField(
        max_digits=19, decimal_places=2, required=False,
        label=_("Annual leasing fee"))
    annual_leasing_fee_currency = forms.ModelChoiceField(
        required=False, label=_("Annual leasing fee currency"),
        queryset=Currency.objects.all().order_by("ranking", "name"))
    annual_leasing_fee_type = forms.TypedChoiceField(
        required=False, label=_("Annual leasing fee type"),
        choices=price_type_choices)
    annual_leasing_fee_area = forms.IntegerField(
        required=False, label=_("Purchase price area"), help_text=_("ha"),
        widget=forms.NumberInput(attrs={'placeholder': _('Size')}))
    tg_leasing_fees_comment = forms.CharField(
        required=False, label=_("Comment on leasing fees"), widget=CommentInput)

    # Contract farming
    tg_contract_farming = TitleField(
        required=False, label="", initial=_("Contract farming"))
    contract_farming = forms.ChoiceField(
        required=False, label=_("Contract farming"),
        choices=CONTRACT_FARMING_CHOICES, widget=forms.RadioSelect)
    on_the_lease = forms.BooleanField(
        required=False, label=_("On leased / purchased area"))
    on_the_lease_area = YearBasedIntegerField(
        required=False, label=_("On leased / purchased area (in ha)"),
        help_text=_("ha"), placeholder=_('Size'))
    on_the_lease_farmers = YearBasedIntegerField(
        required=False, label=_("On leased / purchased farmers"),
        help_text=_("farmers"))
    on_the_lease_households = YearBasedIntegerField(
        required=False, label=_("On leased / purchased households"),
        help_text=_("households"))
    off_the_lease = forms.BooleanField(
        required=False, label=_("Not on leased / purchased area (out-grower)"))
    off_the_lease_area = YearBasedIntegerField(
        required=False, label=_("Not on leased / purchased area (out-grower, in ha)"),
        help_text=_("ha"), placeholder=_('Size'))
    off_the_lease_farmers = YearBasedIntegerField(
        required=False,
        label=_("Not on leased / purchased farmers (out-grower)"),
        help_text=_("farmers"))
    off_the_lease_households = YearBasedIntegerField(
        required=False,
        label=_("Not on leased / purchased households (out-grower)"),
        help_text=_("households"))
    tg_contract_farming_comment = forms.CharField(
        required=False, label=_("Comment on contract farming"),
        widget=CommentInput)

    class Meta:
        name = 'general_information'
