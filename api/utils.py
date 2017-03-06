import collections


class PropertyCounter(dict):
    """
    Helper to count occurrences of defined properties for deals grouped by
    country
    """

    # mapping of keys from elasticsearch <-> map legend.
    properties = {
        'intention': 'intention',
        'implementation': 'negotiation_status',
        'accuracy': 'level_of_accuracy',
    }

    def __init__(self):
        super().__init__()
        self.counter = 0
        for prop in self.properties.keys():
            setattr(self, prop, collections.defaultdict(int))

    def increment(self, **data):
        """
        Increment all counters according to given data from elasticsearch.
        """
        for key, es_key in self.properties.items():
            values = data.get(es_key)
            prop = getattr(self, key)
            if isinstance(values, list):
                for val in values:
                    prop[val] += 1
            else:
                prop[values] += 1
        self.counter += 1

    def get_properties(self):
        return {prop: getattr(self, prop) for prop in self.properties}
