from django.forms.widgets import Select

from landmatrix.models.investor import Investor, InvestorVentureInvolvement
from landmatrix.models.status import Status

from django.utils.translation import ugettext_lazy as _
from django import forms


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


investor_widget = Select(attrs={'class': 'form-control investorfield'})


class ParentStakeholderForm(forms.ModelForm):
    fk_investor = forms.ModelChoiceField(
        required=True, label=_("Existing stakeholder"),
        queryset=Investor.objects.all(), widget=investor_widget)
    percentage = forms.DecimalField(
        required=False, max_digits=5, decimal_places=2,
        label=_("Percentage of investment"), help_text=_("%"))

    class Meta:
        model = InvestorVentureInvolvement
        fields = [
            'id', 'fk_investor', 'loans_amount', 'loans_currency',
            'loans_date',
        ]


class ParentInvestorForm(ParentStakeholderForm):
    fk_investor = forms.ModelChoiceField(
        required=True, label=_("Existing investor"),
        queryset=Investor.objects.all(), widget=investor_widget)

    class Meta:
        model = InvestorVentureInvolvement
        fields = ['id', 'fk_investor', 'percentage']


class BaseInvolvementFormSet(forms.BaseModelFormSet):

    def save(self, fk_venture, commit=True):
        '''
        We are sort of emulating an inline formset here. Save will update
        everything with the relevant associated venture.
        '''
        instances = super().save(commit=False)

        for instance in instances:
            instance.fk_venture = fk_venture
            instance.role = self.ROLE
            instance.fk_status_id = Investor.STATUS_PENDING
            if commit:
                instance.save()

        # Soft delete by setting status to deleted
        if self.deleted_objects:
            for deleted in self.deleted_objects:
                deleted.fk_status_id = Investor.STATUS_DELETED
                if commit:
                    deleted.save()

        return instances


class BaseStakeholderFormSet(BaseInvolvementFormSet):
    ROLE = InvestorVentureInvolvement.STAKEHOLDER_ROLE


class BaseInvestorFormSet(BaseInvolvementFormSet):
    ROLE = InvestorVentureInvolvement.INVESTOR_ROLE


ParentStakeholderFormSet = forms.modelformset_factory(
    InvestorVentureInvolvement, form=ParentStakeholderForm,
    formset=BaseStakeholderFormSet, extra=1, min_num=0, max_num=1,
    can_delete=True)

ParentInvestorFormSet = forms.modelformset_factory(
    InvestorVentureInvolvement, form=ParentInvestorForm,
    formset=BaseInvestorFormSet, extra=1, min_num=0, max_num=1,
    can_delete=True)
