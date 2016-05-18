from pprint import pprint

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country
from landmatrix.models.deal import Deal

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import TitleField, YearBasedIntegerField, CommentInput

from django import forms
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _


class DealContractForm(BaseForm):

    form_title = _('Contracts')

    tg_contract = TitleField(
        required=False, label="", initial=_("Contract")
    )
    contract_number = forms.IntegerField(
        required=False, label=_("Contract number")
    )
    contract_date = forms.DateField(
        required=False, label=_("Contract date"), help_text="[dd:mm:yyyy]",
        input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )
    contract_expiration_date = forms.DateField(
        required=False, label=_("Contract expiration date"), help_text="[dd:mm:yyyy]",
        input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )
    sold_as_deal = forms.IntegerField(
        required=False, label=_("Sold as deal no.")
    )
    tg_negotiation_status_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # Duration of the agreement
    tg_agreement_duration = TitleField(
        required=False, label="", initial=_("Duration of the agreement")
    )
    agreement_duration = YearBasedIntegerField(
        required=False, label=_("Duration of the agreement"), help_text=_("years")
    )
    tg_agreement_duration_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    class Meta:
        name = 'spatial_data'


class DealContractFormSet(formset_factory(DealContractForm, extra=0)):

    form_title = _('Contracts')

    @classmethod
    def get_data(cls, activity):
        if isinstance(activity, Deal):
            activity = activity.activity
        if isinstance(activity, Activity):
            taggroups = ActivityAttributeGroup.objects.\
                filter(fk_activity=activity).filter(attributes__contains=["location"])
        else:
            taggroups = []
        data = []
        for i, taggroup in enumerate(taggroups):
            form_data = DealContractForm.get_data(activity, taggroup=taggroup)
            data.append(form_data)
        return data

    def get_attributes(self, request=None):
        return [form.get_attributes(request) for form in self.forms]

    class Meta:
        name = 'contract_data'
