from django import forms
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _

from grid.fields import TitleField, YearMonthDateField
from grid.widgets import CommentInput
from .base_form import BaseForm


class DealContractForm(BaseForm):

    form_title = _('Contracts')

    tg_contract = TitleField(
        required=False, label="", initial=_("Contract")
    )
    contract_number = forms.CharField(
        required=False, label=_("Contract number")
    )
    contract_date = YearMonthDateField(
        required=False, label=_("Contract date"), help_text="[YYYY-MM-DD]",
    )
    contract_expiration_date = YearMonthDateField(
        required=False, label=_("Contract expiration date"), help_text="[YYYY-MM-DD]",
    )
    sold_as_deal = forms.IntegerField(
        required=False, label=_("Sold as deal no.")
    )
    agreement_duration = forms.IntegerField(
        required=False, label=_("Duration of the agreement (in years)"), help_text=_("years")
    )
    tg_contract_comment = forms.CharField(
        required=False, label=_("Comment on contract"), widget=CommentInput
    )

    class Meta:
        name = 'contract'


class DealContractFormSet(formset_factory(DealContractForm, extra=1, max_num=1)):
    """
    TODO: inherit from BaseFormSet
    """
    form_title = _('Contracts')

    @classmethod
    def get_data(cls, activity, group=None, prefix=None):
        groups = activity.attributes.filter(fk_group__name__startswith=cls.Meta.name).values_list(
            'fk_group__name', flat=True).order_by('fk_group__name').distinct()

        data = []
        for i, group in enumerate(groups):
            form_data = DealContractForm.get_data(activity, group=group)#, prefix='%s-%i' % (cls.Meta.name, i))
            if form_data:
                data.append(form_data)
        return data

    def get_attributes(self, request=None):
        return [form.get_attributes(request) for form in self.forms]

    class Meta:
        name = 'contract'

PublicViewDealContractFormSet = formset_factory(DealContractForm,
                                               formset=DealContractFormSet,
                                               extra=0)
