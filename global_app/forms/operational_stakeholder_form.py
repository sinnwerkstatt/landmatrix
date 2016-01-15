from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from global_app.forms.base_form import BaseForm
from global_app.widgets.title_field import TitleField
from landmatrix.models.country import Country
from landmatrix.models.investor import Investor, InvestorActivityInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class OperationalStakeholderChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return _investor_description(obj)

    def clean(self, value):
        if not Investor.objects.filter(pk=value).exists():
            raise ValidationError('Investor %i does not exist' % value)
        return value


class OperationalStakeholderForm(BaseForm):
    tg_operational_stakeholder = TitleField(required=False, label="", initial=_("Operational Stakeholder"))
    operational_stakeholder = OperationalStakeholderChoiceField(
            required=True, label=_("Existing Operational Stakeholder"),
            queryset=Investor.objects.filter(
                    pk__in=InvestorActivityInvolvement.objects.values('fk_investor_id').distinct()
            ).order_by('name')
    )  # , widget=LivesearchSelect)
    project_name = CharField(required=False, label=_("Name of investment project"), max_length=255)


def _investor_description(investor):
    return _investor_name(investor) + ' (' + _investor_country_name(investor) + ')' + ' ' + _investor_classification(investor)


def _investor_name(investor):
    return investor.name if len(investor.name) <= 80 else investor.name[:80] + '...'


def _investor_country_name(investor):
    return Country.objects.get(pk=investor.fk_country_id).name if investor.fk_country_id else '-'


def _investor_classification(investor):
    return investor.get_classification_display() if investor.classification else '-'

