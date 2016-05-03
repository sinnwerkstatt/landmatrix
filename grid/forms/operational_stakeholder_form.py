from cms.cache import choices
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
        help_text=_("Actors involved in the negotiation / admission process"),# blank=True, null=True
    )
    actors_classification = YearBasedActorField(
        help_text=_("Actors involved in the negotiation / admission process"),# blank=True, null=True
    )
    relationship_to_parent = ChoiceField(
        label=_('Relationship to parent'),
        choices=(
            ('10', 'Subsidiary of parent company'),
            ('20', 'Local branch of parent company'),
            ('30', 'Joint venture of parent companies')
        )
    )
    project_name = CharField(required=False, label=_("Name of investment project"), max_length=255)

    @classmethod
    def get_data(cls, deal, taggroup=None, prefix=""):
        data = MultiValueDict()
        if deal is None:
            return data

        if cls.DEBUG: print('get_data', str(deal)[:100].replace('\n', ' '), '...')
        for (field_name, field) in cls().fields.items():
            prefixed_name = prefix and "%s-%s"%(prefix, field_name) or field_name
            if 'operational_stakeholder' == field_name:
                data[prefixed_name] = deal.operational_stakeholder
            elif 'project_name' in field_name:
                data[prefixed_name] = deal.get_activity_attributes().get('project_name')
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
