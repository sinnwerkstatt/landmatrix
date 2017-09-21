from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms

from landmatrix.models.investor import Investor
from landmatrix.models.country import Country
from grid.forms.base_model_form import BaseModelForm
from grid.widgets import CommentInput
from grid.utils import get_export_value

INVESTOR_CLASSIFICATION_CHOICES = BLANK_CHOICE_DASH + list(
    Investor.INVESTOR_CLASSIFICATIONS)
STAKEHOLDER_CLASSIFICATION_CHOICES = BLANK_CHOICE_DASH + list(
    Investor.STAKEHOLDER_CLASSIFICATIONS)


# TODO: move to fields.
# TODO: Change this to a livesearch widget
class InvestorField(forms.ChoiceField):
    def widget_attrs(self, widget):
        return {'class': 'investorfield'}


class BaseInvestorForm(BaseModelForm):
    # We use ID to build related form links
    id = forms.CharField(required=False, label=_("ID"), widget=forms.HiddenInput())
    name = forms.CharField(required=False, label=_("Name"), max_length=255)
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=INVESTOR_CLASSIFICATION_CHOICES + STAKEHOLDER_CLASSIFICATION_CHOICES)
    fk_country = forms.ModelChoiceField(
        required=False, label=_("Country of registration/origin"),
        queryset=Country.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control countryfield'}))
    comment = forms.CharField(
        required=False, label=_("Comment"), widget=CommentInput)

    class Meta:
        model = Investor
        exclude = ('fk_status', 'subinvestors', 'investor_identifier', 'timestamp')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get('fk_country', self.initial.get('fk_country', None))
        if valid_choice:
            self.fields['fk_country'].queryset = Country.objects.filter(pk=valid_choice)

    def save(self, commit=True):
        '''
        Force status to pending on update.
        '''
        instance = super().save(commit=False)
        instance.fk_status_id = Investor.STATUS_PENDING
        if commit:
            instance.save()

        return instance

    def get_attributes(self, **kwargs):
        return {
            'comment': self.cleaned_data.get('comment'),
        }

    @classmethod
    def get_data(cls, investor):
        return {}

    def clean(self):
        cleaned_data = super(BaseInvestorForm, self).clean()

        # Prevent duplicate names
        # FIXME: Make model field unique in the future
        name = self.cleaned_data['name']
        duplicates = Investor.objects.filter(name=name)
        id = cleaned_data.get('id', None)
        if id:
            duplicates = duplicates.exclude(id=id)
        if duplicates.count() > 0:
            self.add_error('name', "This name exists already.")

        return cleaned_data


class ExportInvestorForm(BaseInvestorForm):
    exclude_in_export = ('id', 'fk_status', 'timestamp', 'subinvestors')

    fk_country = forms.ModelChoiceField(
        required=False, label=_("Country of registration/origin"),
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control countryfield'}))

    @classmethod
    def export(cls, doc, prefix=''):
        """Get field value for export"""
        output = {}
        for field_name, field in cls.base_fields.items():
            field_name = '%s%s' % (prefix, field_name)
            export_key = '%s_export' % field_name

            values = doc.get('%s' % field_name)
            if not values:
                output[export_key] = []
                continue
            if not isinstance(values, (list, tuple)):
                values = [values,]
            # Remove # in name
            if field_name == '%sname' % prefix:
                values = [v.replace('#', '') for v in values]

            output[export_key] = get_export_value(field, values)

        return output

    class Meta:
        model = Investor
        exclude = ()


class ParentInvestorForm(BaseInvestorForm):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=INVESTOR_CLASSIFICATION_CHOICES)

    class Meta:
        model = Investor
        exclude = (
            'fk_status', 'subinvestors', 'investor_identifier',
            'parent_relation', 'timestamp',
        )


class ParentStakeholderForm(ParentInvestorForm):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=STAKEHOLDER_CLASSIFICATION_CHOICES)


class OperationalCompanyForm(BaseInvestorForm):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=STAKEHOLDER_CLASSIFICATION_CHOICES)