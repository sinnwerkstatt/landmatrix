from django.forms.widgets import Select

from landmatrix.models.investor import Investor, InvestorVentureInvolvement
from landmatrix.models.status import Status

from django.utils.translation import ugettext_lazy as _
from django import forms


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


# TODO: shoud we really be limiting stakeholder selection to existing
# investors? How can anyone add a new one?
investor_involvement_ids = InvestorVentureInvolvement.objects.values(
    'fk_investor_id').distinct()
existing_investors = Investor.objects.filter(pk__in=investor_involvement_ids)
existing_investors = existing_investors.order_by('name')
investor_widget = Select(attrs={'class': 'form-control investorfield'})


class ParentStakeholderForm(forms.ModelForm):
    # id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    fk_investor = forms.ModelChoiceField(required=True,
                                         label=_("Existing stakeholder"),
                                         queryset=existing_investors,
                                         widget=investor_widget)
    percentage = forms.DecimalField(required=False, max_digits=5,
                                    decimal_places=2,
                                    label=_("Percentage of investment"),
                                    help_text=_("%"))

    class Meta:
        model = InvestorVentureInvolvement
        fields = ['id', 'fk_investor', 'percentage']


class ParentInvestorForm(ParentStakeholderForm):
    fk_investor = forms.ModelChoiceField(required=True,
                                         label=_("Existing investor"),
                                         queryset=existing_investors,
                                         widget=investor_widget)

    class Meta:
        model = InvestorVentureInvolvement
        fields = ['id', 'fk_investor', 'percentage']


class BaseInvolvementFormSet(forms.BaseModelFormSet):

    def save(self, fk_venture, role, commit=True):
        '''
        We are sort of emulating an inline formset here. Save will update
        everything with the relevant role and associated venture.
        '''
        instances = super().save(commit=False)

        # Status constants would be more efficient but may lead to DB errors
        pending_status = Status.objects.get(name='pending')

        for instance in instances:
            instance.fk_venture = fk_venture
            instance.role = role
            instance.fk_status = pending_status
            if commit:
                instance.save()

        # Soft delete by setting status to deleted
        if self.deleted_objects:
            deleted_status = Status.objects.get(name='deleted')
            for deleted in self.deleted_objects:
                deleted.fk_status = deleted_status
                if commit:
                    deleted.save()

        return instances


ParentStakeholderFormSet = forms.modelformset_factory(
    InvestorVentureInvolvement, form=ParentStakeholderForm,
    formset=BaseInvolvementFormSet, extra=1, min_num=0, can_delete=True)

ParentInvestorFormSet = forms.modelformset_factory(
    InvestorVentureInvolvement, form=ParentInvestorForm,
    formset=BaseInvolvementFormSet, extra=1, min_num=0, can_delete=True)
