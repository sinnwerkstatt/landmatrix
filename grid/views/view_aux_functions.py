from pprint import pprint
import json

from django.template import loader
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _

from api.filters import FILTER_VAR_ACT, FILTER_VAR_INV
from landmatrix.models.country import Country
from grid.views.browse_condition_form import BrowseConditionForm
from grid.views.save_deal_view import SaveDealView


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def create_condition_formset():
    ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
    ConditionFormset.form = staticmethod(
        curry(BrowseConditionForm, variables_activity=FILTER_VAR_ACT, variables_investor=FILTER_VAR_INV)
    )
    return ConditionFormset


def render_to_response(template_name, context, context_instance):
    """ Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments."""
    # Some deprecated arguments were passed - use the legacy code path
    return HttpResponse(render_to_string(template_name, context, context_instance))


def render_to_string(template_name, context, context_instance):
    return loader.render_to_string(template_name, context, context_instance)


def get_field_label(name):
    CUSTOM_FIELDS = {
        'activity_identifier': _('Deal ID')
    }
    if name in CUSTOM_FIELDS.keys():
        return str(CUSTOM_FIELDS[name])
    label = None
    for form in SaveDealView.FORMS:
        # Formset?
        if hasattr(form, 'form'):
            form = form.form
        if name in form.base_fields:
            label = str(form.base_fields.get(name).label)
            break
    return label
