from django.forms.models import ModelChoiceField
from django.forms.widgets import Select
from grid.forms.base_form import BaseForm
from grid.forms.investor_form import InvestorField
from grid.forms.operational_stakeholder_form import investor_description

from landmatrix.models.investor import Investor, InvestorVentureInvolvement

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.formsets import formset_factory

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ParentStakeholderForm(BaseForm):

    # stakeholder = InvestorField(required=False, label=_("Existing investor"), choices=())
    stakeholder = ModelChoiceField(
            required=True, label=_("Existing stakeholder"),
            queryset=Investor.objects.filter(
                    pk__in=InvestorVentureInvolvement.objects.values('fk_investor_id').distinct()
            ).order_by('name'),
            widget=Select(
                attrs={'class': 'form-control investorfield'}
            )
    )
    percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})

        investor = initial.pop("stakeholder", None)
        if isinstance(investor, list) and len(investor):
            investor = investor[0]
        self.fields["stakeholder"].initial = investor

    def _fill_investor_choices(self):
        self.investor_choices = [
            (investor.id, investor_description(investor))
            for investor in Investor.objects.filter(fk_status_id__in=(2, 3)).order_by('name')
        ]
        self.fields["stakeholder"].choices = list(self.fields["stakeholder"].choices)[:1]
        self.fields["stakeholder"].choices.extend(self.investor_choices)

    @classmethod
    def get_data(cls, investor_id, _=None, __=None):
        data = super().get_data(investor_id)
        data['stakeholder'] = investor_id
        return data


class ParentInvestorForm(BaseForm):

    # parent_investor = InvestorField(required=False, label=_("Existing investor"), choices=())
    parent_investor = ModelChoiceField(
            required=True, label=_("Existing investor"),
            queryset=Investor.objects.filter(
                    pk__in=InvestorVentureInvolvement.objects.values('fk_investor_id').distinct()
            ).order_by('name'),
            widget=Select(
                attrs={'class': 'form-control investorfield'},
            )
    )
    parent_investor_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})

        investor = initial.pop("parent_investor", None)
        if isinstance(investor, list) and len(investor):
            investor = investor[0]
        self.fields["parent_investor"].initial = investor
        #self._fill_investor_choices()

    def _fill_investor_choices(self):
        self.investor_choices = [
            (investor.id, investor_description(investor))
            for investor in Investor.objects.filter(fk_status_id__in=(2, 3)).order_by('name')
        ]
        self.fields["parent_investor"].choices = list(self.fields["parent_investor"].choices)[:1]
        self.fields["parent_investor"].choices.extend(self.investor_choices)

    @classmethod
    def get_data(cls, investor_id, _=None, __=None):
        data = super().get_data(investor_id)
        data['parent_investor'] = investor_id
        return data


class ParentStakeholderFormSet(formset_factory(ParentStakeholderForm, extra=0, min_num=1)):

    @classmethod
    def get_data(cls, investor, role):
        parent_investors = InvestorVentureInvolvement.objects.filter(fk_venture=investor).filter(role=role).\
            values_list('fk_investor_id', flat=True).distinct()

        if not parent_investors:
            return []

        data = [None]*len(parent_investors)
        for i, parent_investor in enumerate(parent_investors):
            data[i] = ParentStakeholderForm.get_data(parent_investor)

        return data


class ParentInvestorFormSet(formset_factory(ParentInvestorForm, extra=0, min_num=1)):

    @classmethod
    def get_data(cls, investor, role):
        parent_investors = InvestorVentureInvolvement.objects.filter(fk_venture=investor).filter(role=role).\
            values_list('fk_investor_id', flat=True).distinct()

        if not parent_investors:
            return []

        data = [None]*len(parent_investors)
        for i, parent_investor in enumerate(parent_investors):
            data[i] = ParentInvestorForm.get_data(parent_investor)

        print('ParentInvestorForm.get_data():', data)

        return data
