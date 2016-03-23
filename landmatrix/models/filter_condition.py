from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.query_sets.sql_generation.filter_to_sql import FilterToSQL
from landmatrix.models.filter_preset import FilterPreset

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


def get_filter_vars():
    return FILTER_VAR_ACT+FILTER_VAR_INV


class FilterCondition(models.Model):
    fk_rule = models.ForeignKey(FilterPreset)
    variable = models.CharField(
        _("Variable"), max_length=32,
        choices=([(var, ' '.join(v.title() for v in var.split('_'))) for var in get_filter_vars()])
    )
    operator = models.CharField(
        _("Operator"), max_length=10,
        choices=((key, key) for key in FilterToSQL.OPERATION_MAP.keys())
    )
    value = models.CharField(_("Value"), max_length=1024)

    def __str__(self):
        return '{} {} {}'.format(self.variable, self.operator, self.value)

    def to_filter(self):
        from api.views.filter import Filter
        return Filter(self.variable, self.operator, self.value, str(self))

    def __getitem__(self, item):
        if item == 'variable':
            return [self.variable]
        elif item == 'operator':
            return [self.operator]
        elif item == 'value':
            return [self.parsed_value]
        raise ValueError('FilterCondition<{}>[{}]'.format(str(self), item))

    @property
    def parsed_value(self):
        if ',' in self.value:
            return [v.strip() for v in self.value.split(',')]
        return self.value
