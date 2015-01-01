from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms.fields import ChoiceField
from django.forms.widgets import Select
from django.forms.models import ModelChoiceField
from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext_lazy as _

from grid.forms.base_form import BaseForm
from grid.widgets.title_field import TitleField
from grid.widgets.year_based_checkbox_input import YearBasedCheckboxInput
from grid.widgets.year_based_integer_field import YearBasedActorField
from grid.widgets.year_based_text_input import YearBasedTextInput
from landmatrix.models.country import Country
from landmatrix.models.investor import Investor, InvestorActivityInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class OperationalStakeholderForm(BaseForm):

    form_title = _('Investor info')

    tg_operational_stakeholder = TitleField(required=False, label="", initial=_("Operational Stakeholder"))
    operational_stakeholder = ModelChoiceField(
            required=True, label=_("Existing Operational Stakeholder"),
            queryset=Investor.objects.filter(
                    pk__in=InvestorActivityInvolvement.objects.values('fk_investor_id').distinct()
            ).order_by('name'),
            widget=Select(
                attrs={'class': 'form-control investorfield'}
            )
    )
    actors_involved = YearBasedActorField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),# blank=True, null=True
    )
    actors_classification = YearBasedActorField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),# blank=True, null=True
    )
    relationship_to_parent = ChoiceField(
        label=_('Relationship to parent'),
        required=False,
        choices=(
            (_('Subsidiary of parent company'), _('Subsidiary of parent company')),
            (_('Local branch of parent company'), _('Local branch of parent company')),
            (_('Joint venture of parent companies'), _('Joint venture of parent companies'))
        )
    )
    project_name = CharField(required=False, label=_("Name of investment project"), max_length=255)

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group, prefix)
        op = InvestorActivityInvolvement.objects.filter(fk_activity_id=activity.id).first()
        if op:
            data['operational_stakeholder'] = op
        #elif 'project_name' in field_name:
        #    project_name = activity.attributes.get(name='project_name')
        #    data[prefixed_name] = activity.attributes.get(name='project_name').value
        return data

    class Meta:
        name = 'investor_info'

def investor_description(investor):
    return '{} ({}) {}'.format(
        _investor_name(investor), _investor_country_name(investor), _investor_classification(investor)
    )

def _investor_name(investor):
    return investor.name if len(investor.name) <= 80 else investor.name[:80] + '...'

def _investor_country_name(investor):
    return investor.fk_country.name if investor.fk_country_id else '-'

def _investor_classification(investor):
    return investor.get_classification_display() if investor.classification else '-'
