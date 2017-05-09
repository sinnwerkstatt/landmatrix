from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms

from landmatrix.models.investor import Investor
from landmatrix.models.country import Country
from grid.forms.base_model_form import BaseModelForm
from grid.widgets import CommentInput


INVESTOR_CLASSIFICATION_CHOICES = BLANK_CHOICE_DASH + list(
    Investor.INVESTOR_CLASSIFICATIONS)
STAKEHOLDER_CLASSIFICATION_CHOICES = BLANK_CHOICE_DASH + list(
    Investor.STAKEHOLDER_CLASSIFICATIONS)


# TODO: move to fields.
# TODO: Change this to a livesearch widget
class InvestorField(forms.ChoiceField):
    def widget_attrs(self, widget):
        return {'class': 'investorfield'}


class InvestorFormBase(BaseModelForm):
    # We use ID to build related form links
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False, label=_("Name"), max_length=255)
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=INVESTOR_CLASSIFICATION_CHOICES)
    fk_country = forms.ModelChoiceField(
        required=False, label=_("Country of registration/origin"),
        queryset=Country.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control countryfield'}))
    comment = forms.CharField(
        required=False, label=_("Comment"), widget=CommentInput)

    class Meta:
        model = Investor
        exclude = ('fk_status', 'subinvestors', 'investor_identifier', 'timestamp')

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


class InvestorForm(InvestorFormBase):
    class Meta:
        model = Investor
        exclude = (
            'fk_status', 'subinvestors', 'investor_identifier',
            'parent_relation', 'timestamp',
        )


class StakeholderForm(InvestorForm):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=STAKEHOLDER_CLASSIFICATION_CHOICES)


class OperationalCompanyForm(InvestorFormBase):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=STAKEHOLDER_CLASSIFICATION_CHOICES)
