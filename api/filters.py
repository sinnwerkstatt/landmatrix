from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country
from landmatrix.models.filter_preset import FilterPreset
from api.query_sets.sql_generation.filter_to_sql import FilterToSQL


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
FILTER_VAR_INV = ['investor', "operational_stakeholder_name", "country", 'operational_stakeholder_country']
# TODO: this counter is shared by all users, and is per thread.
# It should probably be moved to the session
FILTER_COUNTER = 0


def generate_filter_name():
    global FILTER_COUNTER
    FILTER_COUNTER += 1
    return 'filter_{}'.format(FILTER_COUNTER)


# TODO: convert to object, these don't need to be dicts.
class BaseFilter(dict):
    ACTIVITY_TYPE = 'activity'
    INVESTOR_TYPE = 'investor'

    @property
    def name(self):
        return self['name']

    @property
    def type(self):
        if self['name'] in FILTER_VAR_INV:
            filter_type = self.INVESTOR_TYPE
        else:
            filter_type = self.ACTIVITY_TYPE

        return filter_type


class Filter(BaseFilter):

    def __init__(
            self, variable, operator, value, name=None, label=None, key=None):
        if operator not in FilterToSQL.OPERATION_MAP:
            raise ValueError('No such operator: {}'.format(operator))

        if name is None:
            name = generate_filter_name()

        super().__init__(name=name, variable=variable, operator=operator,
                         value=value, label=label, key=key)

    @classmethod
    def from_session(cls, filter_dict):
        '''
        Because filters inherit from dict, they are stored in the session
        as dicts.
        '''
        return cls(
            filter_dict['variable'], filter_dict['operator'],
            filter_dict['value'], name=filter_dict.get('name'),
            label=filter_dict.get('label'), key=filter_dict.get('key'))

    def to_sql_format(self):
        """
        Converts a filter into the format used by FilterToSql:
        {'variable__operator': value}
        """
        key = self['key'] or 'value'
        # TODO: hopefully _parse_value is no longer required
        value = _parse_value(self['value'])
        # Is this still required? Why not just always store ids?
        is_country_string = (
            'country' in self['variable'] and
            key == 'value' and
            not value.isnumeric()
        )
        if is_country_string:
            country = Country.objects.get(name__iexact=value.replace('-', ' '))
            value = str(country.pk)
        if 'in' in self['operator'] and not isinstance(value, list):
            value = [value]

        definition_key = '__'.join(
            (self['variable'], self['key'], self['operator']))
        formatted_filter = {
            definition_key: value,
        }

        return formatted_filter


class PresetFilter(BaseFilter):

    def __init__(self, preset_id, name=None, label=None):
        self.preset_id = preset_id
        # Store this obj during init, rather than doing seperate validation
        # and a get method
        self.filter = FilterPreset.objects.get(id=self.preset_id)

        if name is None:
            name = generate_filter_name()

        if label is None:
            label = self.filter.name

        super().__init__(name=name, preset_id=self.preset_id, label=label)

    @classmethod
    def from_session(cls, filter_dict):
        '''
        Because filters inherit from dict, they are stored in the session
        as dicts.
        '''
        return cls(
            filter_dict['preset_id'], name=filter_dict.get('name'),
            label=filter_dict.get('label'))


def format_filters(filters):
    '''
    Format filters as expected by FilterToSQL and ActivityQueryset.
    '''
    # TODO: cleanup and move to FilterToSQL
    formatted_filters = {
        'activity': {'tags': {}},
        'investor': {'tags': {}},
    }

    def _update_filters(filter_dict, filter, group=None):
        name = filter[1].type
        definition = filter[1].to_sql_format()
        definition_key = list(definition.keys())[0]
        if group:
            if group not in filter_dict[name]['tags']:
                filter_dict[name]['tags'][group] = {}
            tags = filter_dict[name]['tags'][group]
        else:
            tags = filter_dict[name]['tags']
        if filter[1]['variable'] == 'deal_scope':
            filter_dict['deal_scope'] = filter[1].value
        elif filter_dict[name]['tags'].get(definition_key) and isinstance(filter_dict[name]['tags'][definition_key], list):
            tags[definition_key].extend(definition[definition_key])
        else:
            tags.update(definition)

    for filter_name, filter_obj in filters.items():
        if isinstance(filter_obj, PresetFilter):
            conditions = filter_obj.filter.conditions.all()
            for i, condition in enumerate(conditions):
                if filter_obj.filter.relation == filter_obj.filter.RELATION_AND:
                    group = None
                else:
                    group = filter_obj.name
                _update_filters(
                    formatted_filters,
                    ('{}_{}'.format(filter_obj.name, i), condition.to_filter()),
                    group=group)
        else:
            _update_filters(formatted_filters, filter_obj)

    return formatted_filters


def load_filters(request):
    filters = {}
    for filter_name, filter_dict in request.session.get('filters', {}).items():
        if 'preset_id' in filter_dict:
            filters[filter_name] = PresetFilter.from_session(filter_dict)
        else:
            filters[filter_name] = Filter.from_session(filter_dict)

    filters.update(load_filters_from_url(request))
    formatted_filters = format_filters(filters)

    return formatted_filters


def load_filters_from_url(request):
    '''
    Read any querystring param filters. Preset filters not allowed.
    '''
    variables = request.GET.getlist('variable')
    operators = request.GET.getlist('operator')
    values = request.GET.getlist('value')
    combined = zip(variables, operators, values)

    filters = {f[0]: Filter(f[0], f[1], f[2]) for f in combined}

    return filters


def _parse_value(filter_value):
    """
    Necessary due to the different ways single values and lists are stored
    in DB and session.
    """
    if len(filter_value) > 1:
        return filter_value
    if filter_value:
        value = filter_value[0]
    else:
        value = ''
    if '[' in value:
        value = [str(v) for v in json.loads(value)]
    return value
