
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Filter(dict):

    filter_number = 0

    def __init__(self, variable, operator, value, name=None):
        Filter.filter_number += 1
        super().__init__(
            {'name': name if name else 'filter_{}'.format(Filter.filter_number),
             'variable': variable, 'operator': operator, 'value': value}
        )

    @property
    def name(self):
        return self['name']

