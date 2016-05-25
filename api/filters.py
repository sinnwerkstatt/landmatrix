from api.query_sets.sql_generation.filter_to_sql import FilterToSQL
from landmatrix.models.filter_preset import FilterPreset


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


# TODO: this counter is shared by all users, and is per thread.
# It should probably be moved to the session
FILTER_COUNTER = 0


def generate_filter_name():
    global FILTER_COUNTER
    FILTER_COUNTER += 1
    return 'filter_{}'.format(FILTER_COUNTER)


class Filter(dict):

    def __init__(self, variable, operator, value, name=None, label=None):
        if operator not in FilterToSQL.OPERATION_MAP:
            raise ValueError('No such operator: {}'.format(operator))

        if name is None:
            name = generate_filter_name()

        super().__init__(name=name, variable=variable, operator=operator,
                         value=value, label=label)

    @property
    def name(self):
        return self['name']


class PresetFilter(dict):

    def __init__(self, preset_id, name=None, label=None):
        self.preset_id = preset_id
        # Store this obj during init, rather than doing seperate validation
        # and a get method
        self.filter = FilterPreset.objects.get(id=self.preset_id)

        if name is None:
            name = generate_filter_name()

        super().__init__(name=name, preset_id=self.preset_id, label=label)

    @property
    def name(self):
        return self['name']
