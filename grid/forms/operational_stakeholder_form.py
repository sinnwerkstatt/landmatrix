from django import forms
from django.forms.widgets import Select
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.investor import Investor, InvestorActivityInvolvement
from grid.forms.base_form import BaseForm
from grid.forms.choices import actor_choices
from grid.fields import TitleField, ActorsField
from grid.widgets import CommentInput


class OperationalStakeholderForm(BaseForm):
    exclude_in_export = ('operational_stakeholder',)

    form_title = _('Investor info')

    tg_operational_stakeholder = TitleField(
        required=False, label="", initial=_("Operational company"))
    operational_stakeholder = ModelChoiceField(
        required=False, label=_("Operational company"),
        queryset=Investor.objects.none(),
        widget=Select(attrs={'class': 'form-control investorfield'}))
    actors = ActorsField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),
        choices=actor_choices)
    project_name = forms.CharField(
        required=False, label=_("Name of investment project"), max_length=255)
    tg_operational_stakeholder_comment = forms.CharField(
        required=False, label=_("Comment on Operational company"),
        widget=CommentInput)

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group, prefix)
        op = InvestorActivityInvolvement.objects.filter(
            fk_activity__activity_identifier=activity.activity_identifier).first()
        if op:
            data['operational_stakeholder'] = str(op.fk_investor.id)
        return data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get('operational_stakeholder', self.initial.get('operational_stakeholder', None))
        if valid_choice:
            self.fields['operational_stakeholder'].queryset = Investor.objects.filter(pk=valid_choice)

    class Meta:
        name = 'investor_info'