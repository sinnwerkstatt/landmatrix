import datetime

from landmatrix.models.deal_history import DealHistoryItem


def _get_added_attributes(earlier_deal, later_deal):
    added = {}

    earlier_attrs = set(earlier_deal.attributes.keys())
    later_attrs = set(later_deal.attributes.keys())
    added_attrs = later_attrs - earlier_attrs

    for attr_name in added_attrs:
        later_value = later_deal.attributes[attr_name]
        if later_value not in (None, ''):
            added[attr_name] = (None, later_value)

    return added


def _get_changed_or_removed_attributes(earlier_deal, later_deal):
    changes = {}

    for attr_name, earlier_value in earlier_deal.attributes.items():
        try:
            later_value = later_deal.attributes[attr_name]
        except KeyError:
            later_value = None

        unequal = earlier_value != later_value
        both_empty = earlier_value in (None, '') and later_value in (None, '')
        if unequal and not both_empty:
            changes[attr_name] = (earlier_value, later_value)

    return changes


class DealChangesList:
    '''
    An iterator to go over deal history.
    '''

    def __init__(self, deal, max_items=100):
        self.deal = deal
        deal_history = DealHistoryItem.get_history_for(self.deal)
        self.deal_history = list(deal_history.items())

    def __iter__(self):
        self.index = 0
        self.later_deal = None
        self.later_deal_timestamp = None

        initial_timestamp, initial_deal = self.deal_history[self.index]
        self.earlier_deal = initial_deal
        self.earlier_deal_timestamp = initial_timestamp

        return self

    def compare_deals(self):
        '''
        Returns a dict of (old, new) value tuples.
        '''
        changes = _get_changed_or_removed_attributes(self.earlier_deal,
                                                     self.later_deal)
        changes.update(
            _get_added_attributes(self.earlier_deal, self.later_deal))

        # Operational stakeholder is not in attributes
        if (self.earlier_deal.operational_stakeholder !=
           self.later_deal.operational_stakeholder):
            changes['operational_stakeholder'] = (
                self.earlier_deal.operational_stakeholder,
                self.later_deal.operational_stakeholder,
            )

        return changes

    def __next__(self):
        self.later_deal = self.earlier_deal
        self.later_deal_timestamp = self.earlier_deal_timestamp

        self.index += 1

        try:
            next_timestamp, next_deal = self.deal_history[self.index]
        except IndexError:
            raise StopIteration
        else:
            self.earlier_deal = next_deal
            self.earlier_deal_timestamp = next_timestamp

        changes = self.compare_deals()
        deal_datetime = datetime.datetime.utcfromtimestamp(
            self.later_deal_timestamp)

        return deal_datetime, self.later_deal, changes
