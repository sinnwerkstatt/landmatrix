from django.utils.translation import ugettext_lazy as _
from django import forms

from landmatrix.models.investor import HistoricalInvestor, HistoricalInvestorVentureInvolvement
from grid.fields import TitleField
from grid.forms.base_form import FieldsDisplayFormMixin
from grid.widgets import CommentInput
from grid.utils import get_display_value


class InvestorVentureInvolvementForm(forms.ModelForm):
    exclude_in_export = ('id', 'fk_status', 'timestamp')

    @classmethod
    def get_display_properties(cls, doc):
        """Get field value for export"""
        output = {}
        for field_name, field in cls.base_fields.items():
            key = '%s_display' % field_name
            values = doc.get(field_name)
            if not values:
                output[key] = ''
                continue
            if not isinstance(values, (list, tuple)):
                values = [values,]
            value = get_display_value(field, values)
            if value:
                output[key] = value
        return output

    class Meta:
        model = HistoricalInvestorVentureInvolvement
        exclude = []


class ParentCompanyForm(FieldsDisplayFormMixin,
                        InvestorVentureInvolvementForm):

    form_title = _('Parent companies')

    tg_parent_stakeholder = TitleField(
        required=False, label="", initial=_("Parent company")
    )
    fk_investor = forms.ModelChoiceField(
        required=False, label=_("Existing parent company"),
        queryset=HistoricalInvestor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control investorfield'}))
    percentage = forms.DecimalField(
        required=False, max_digits=5, decimal_places=2,
        label=_("Ownership share"), help_text=_("%"))
    comment = forms.CharField(
        required=False, label=_("Comment"),
        widget=CommentInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get('%s-fk_investor' % self.prefix, self.initial.get(
            'fk_investor', None))
        if valid_choice:
            self.fields['fk_investor'].queryset = HistoricalInvestor.objects.filter(
                pk=valid_choice)

    class Meta:
        name = 'parent-company'
        model = HistoricalInvestorVentureInvolvement
        fields = [
            'tg_parent_stakeholder', 'id', 'fk_investor', 'investment_type', 'percentage',
            'loans_amount', 'loans_date',
            'comment',
        ]


class ParentInvestorForm(ParentCompanyForm):

    form_title = _('Tertiary investor/lender')

    tg_parent_stakeholder = TitleField(
        required=False, label="", initial=_("Tertiary investor/lender")
    )
    fk_investor = forms.ModelChoiceField(
        required=False, label=_("Existing investor"),
        queryset=HistoricalInvestor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control investorfield'}))

    class Meta:
        name = 'parent-investor'
        model = HistoricalInvestorVentureInvolvement
        fields = [
            'tg_parent_stakeholder', 'id', 'fk_investor', 'investment_type', 'percentage',
            'loans_amount', 'loans_date',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get('%s-fk_investor' % self.prefix, self.initial.get(
            'fk_investor', None))
        if valid_choice:
            self.fields['fk_investor'].queryset = HistoricalInvestor.objects.filter(
                pk=valid_choice)


class BaseInvolvementFormSet(forms.BaseModelFormSet):

    def save(self, fk_venture, commit=True):
        '''
        We are sort of emulating an inline formset here. Save will update
        everything with the relevant associated venture.
        '''
        instances = super().save(commit=False)

        for instance in instances:
            if not hasattr(instance, 'fk_investor'):
                continue
            instance.fk_venture = fk_venture
            instance.role = self.ROLE
            instance.fk_status_id = HistoricalInvestor.STATUS_PENDING
            if commit:
                instance.save()

        # Soft delete by setting status to deleted
        if self.deleted_objects:
            for deleted in self.deleted_objects:
                deleted.fk_status_id = HistoricalInvestor.STATUS_DELETED
                if commit:
                    deleted.save()

        return instances


class BaseCompanyFormSet(BaseInvolvementFormSet):
    form_title = _('Parent companies')
    ROLE = HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE

    class Meta:
        name = 'parent-company'


class BaseInvestorFormSet(BaseInvolvementFormSet):
    form_title = _('Tertiary investors/lenders')
    ROLE = HistoricalInvestorVentureInvolvement.INVESTOR_ROLE

    class Meta:
        name = 'parent-investor'


ParentCompanyFormSet = forms.modelformset_factory(
    HistoricalInvestorVentureInvolvement, form=ParentCompanyForm,
    formset=BaseCompanyFormSet, extra=1, min_num=0, max_num=1,
    can_delete=True)

ParentInvestorFormSet = forms.modelformset_factory(
    HistoricalInvestorVentureInvolvement, form=ParentInvestorForm,
    formset=BaseInvestorFormSet, extra=1, min_num=0, max_num=1,
    can_delete=True)
