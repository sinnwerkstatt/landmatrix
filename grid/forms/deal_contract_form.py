from django import forms
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _

from grid.widgets import TitleField, CommentInput
from .base_form import BaseForm


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealContractForm(BaseForm):

    form_title = _('Contracts')

    tg_contract = TitleField(
        required=False, label="", initial=_("Contract")
    )
    contract_number = forms.IntegerField(
        required=False, label=_("Contract number")
    )
    contract_date = forms.DateField(
        required=False, label=_("Contract date"), help_text="[YYYY-MM-DD]",
        input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )
    contract_expiration_date = forms.DateField(
        required=False, label=_("Contract expiration date"), help_text="[YYYY-MM-DD]",
        input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )
    sold_as_deal = forms.IntegerField(
        required=False, label=_("Sold as deal no.")
    )
    agreement_duration = forms.IntegerField(
        required=False, label=_("Duration of the agreement"), help_text=_("years")
    )
    tg_contract_comment = forms.CharField(
        required=False, label=_("Contract comments"), widget=CommentInput
    )

    class Meta:
        name = 'contract'


class DealContractFormSet(formset_factory(DealContractForm, extra=1, max_num=1)):
    '''
    TODO: inherit from BaseFormSet
    '''
    form_title = _('Contracts')
    prefix = 'contract'

    @classmethod
    def get_data(cls, activity, group=None, prefix=None):
        groups = activity.attributes.filter(fk_group__name__startswith=cls.prefix).values_list('fk_group__name').distinct()

        data = []
        for i, group in enumerate(groups):
            form_data = DealContractForm.get_data(activity, group=group[0])#, prefix='contract-%i' % i)
            if form_data:
                data.append(form_data)
        return data

    def get_attributes(self, request=None):
        return [form.get_attributes(request) for form in self.forms]

    class Meta:
        name = 'contract_data'

PublicViewDealContractFormSet = formset_factory(DealContractForm,
                                               formset=DealContractFormSet,
                                               extra=0)
