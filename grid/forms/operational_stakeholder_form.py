from django import forms
from django.forms.widgets import Select
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from grid.forms.base_form import BaseForm
from grid.forms.choices import actor_choices
from grid.widgets import TitleField, CommentInput, ActorsField
from landmatrix.models.investor import Investor, InvestorActivityInvolvement


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class OperationalStakeholderForm(BaseForm):
    # TODO: move queryset to manager
    OPERATIONAL_STAKEHOLDER_IDS = InvestorActivityInvolvement.objects.values(
        'fk_investor_id').distinct()
    STAKEHOLDER_QUERYSET = Investor.objects.filter(
        pk__in=OPERATIONAL_STAKEHOLDER_IDS).order_by('name')
    form_title = _('Investor info')

    tg_operational_stakeholder = TitleField(
        required=False, label="", initial=_("Operational company"))
    operational_stakeholder = ModelChoiceField(
        required=True, label=_("Operational company"),
        queryset=STAKEHOLDER_QUERYSET,
        widget=Select(attrs={'class': 'form-control investorfield'}))
    actors = ActorsField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),
        choices=actor_choices)
    project_name = forms.CharField(
        required=False, label=_("Name of investment project"), max_length=255)
    tg_operational_stakeholder_comment = forms.CharField(
        required=False, label=_("Operational stakeholder comments"),
        widget=CommentInput)

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group, prefix)
        op = InvestorActivityInvolvement.objects.filter(
            fk_activity_id=activity.id).first()
        if op:
            data['operational_stakeholder'] = op.fk_investor.id

        return data

    class Meta:
        name = 'investor_info'


def investor_description(investor):
    return '{} ({}) {}'.format(
        _investor_name(investor), _investor_country_name(investor),
        _investor_classification(investor))


def _investor_name(investor):
    return investor.name if len(investor.name) <= 80 else investor.name[:80] + '...'


def _investor_country_name(investor):
    return investor.fk_country.name if investor.fk_country_id else '-'


def _investor_classification(investor):
    return investor.get_classification_display() if investor.classification else '-'
