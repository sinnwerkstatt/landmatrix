from api.query_sets.sql_generation.filter_to_sql import FilterToSQL
from grid.views.view_aux_functions import FILTER_VAR_INV, FILTER_VAR_ACT

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Filter(dict):

    filter_number = 0

    def __init__(self, variable, operator, value, name=None):

        if operator[0] not in FilterToSQL.OPERATION_MAP:
            raise ValueError('No such operator: {}'.format(operator))
        if variable[0] not in FILTER_VAR_INV and variable not in FILTER_VAR_ACT:
            raise ValueError('No such variable: {}'.format(variable))

        Filter.filter_number += 1
        super().__init__(
            {'name': name if name else 'filter_{}'.format(Filter.filter_number),
             'variable': variable, 'operator': operator, 'value': value}
        )

    @property
    def name(self):
        return self['name']

