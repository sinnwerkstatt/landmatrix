from grid.views.browse_condition_form import BrowseConditionForm

from django.template import loader
from django.http import HttpResponse

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


FILTER_VAR_ACT = [
    "target_country", "location", "intention", "intended_size", "contract_size", "production_size",
    "negotiation_status", "implementation_status", "crops", "nature", "contract_farming", "url", "type", "company",
    "type"
]
FILTER_NEW = [
    "agreement_duration", "animals", "annual_leasing_fee", "annual_leasing_fee_area",
    "annual_leasing_fee_currency", "annual_leasing_fee_type", "community_benefits",
    "community_compensation", "community_consultation", "community_reaction",
    "company", "contract_date", "contract_farming", "contract_number", "contract_size",
    "crops", "date", "deal_scope", "domestic_jobs_created", "domestic_jobs_current",
    "domestic_jobs_current_daily_workers", "domestic_jobs_current_employees",
    "domestic_jobs_planned", "domestic_jobs_planned_daily_workers",
    "domestic_jobs_planned_employees", "domestic_use", "email", "export",
    "export_country1", "export_country1_ratio", "export_country2", "export_country2_ratio",
    "export_country3", "file", "foreign_jobs_created", "foreign_jobs_current",
    "foreign_jobs_current_employees", "foreign_jobs_planned", "foreign_jobs_planned_employees",
    "has_domestic_use", "has_export", "implementation_status", "includes_in_country_verified_information",
    "in_country_processing", "intended_size", "intention", "land_cover", "land_owner", "land_use",
    "level_of_accuracy", "location", "minerals", "name", "nature", "negotiation_status", "not_public",
    "not_public_reason", "number_of_displaced_people", "off_the_lease", "off_the_lease_area",
    "off_the_lease_farmers", "on_the_lease", "on_the_lease_area", "on_the_lease_farmers",
    "phone", "point_lat", "point_lon", "production_size", "project_name", "purchase_price",
    "purchase_price_area", "purchase_price_currency", "purchase_price_type",
    "source_of_water_extraction", "target_country", "total_jobs_created", "total_jobs_current",
    "total_jobs_current_daily_workers", "total_jobs_current_employees", "total_jobs_planned",
    "total_jobs_planned_daily_workers", "total_jobs_planned_employees", "type", "url",
    "water_extraction_amount", "water_extraction_envisaged"
]
FILTER_VAR_INV = ["investor_name", "country"]


def create_condition_formset():
    from django.forms.formsets import formset_factory
    from django.utils.functional import curry

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


def get_filter_name(filter_data):
    if filter_data[0] in FILTER_VAR_INV:
        return 'investor'
    return 'activity'


def get_filter_definition(filter_data):
    filter_data = filter_data[1]
    value = parse_value(filter_data['value'])
    variable = filter_data['variable'][0]
    operator = filter_data['operator'][0]
    return {'{}__{}'.format(variable, operator): value}


def parse_value(filter_value):
    if len(filter_value) > 1:
        return filter_value
    value = filter_value[0]
    if '[' in value:
        value = [str(v) for v in json.loads(value)]
    return value
