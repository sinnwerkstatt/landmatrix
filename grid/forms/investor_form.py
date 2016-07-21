from django.utils.translation import ugettext_lazy as _
from django import forms

from landmatrix.models.investor import Investor
from landmatrix.models.status import Status
from grid.forms.base_model_form import BaseModelForm
from grid.widgets import CommentInput
from grid.forms.choices import operational_company_choices, investor_choices

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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
        choices=(('', _("---------")),) + investor_choices)
    comment = forms.CharField(
        required=False, label=_("Comment"), widget=CommentInput)

    class Meta:
        model = Investor
        exclude = ('fk_status', 'subinvestors', 'investor_identifier')

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
            'parent_relation',
        )


class OperationalCompanyForm(InvestorFormBase):
    classification = forms.ChoiceField(
        required=False, label=_("Classification"),
        choices=(('', _("---------")),) + operational_company_choices)
