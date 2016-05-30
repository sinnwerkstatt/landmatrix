from collections import deque

from landmatrix.models import Deal


def _get_added_attributes(earlier_deal, later_deal):
    added = {}

    earlier_attrs = set(earlier_deal.attributes.keys())
    later_attrs = set(later_deal.attributes.keys())
    added_attrs = later_attrs - earlier_attrs

    for attr_name in added_attrs:
        later_value = later_deal.attributes[attr_name]
        added[attr_name] = (None, later_value)

    return added


def _get_changed_or_removed_attributes(earlier_deal, later_deal):
    changes = {}

    for attr_name, earlier_value in earlier_deal.attributes.items():
        try:
            later_value = later_deal.attributes[attr_name]
        except KeyError:
            later_value = None
        if earlier_value != later_value:
            changes[attr_name] = (earlier_value, later_value)

    return changes


class DealChangesList:
    '''
    An iterator to go over deal history.
    '''

    def __init__(self, deal, max_items=100):
        self.deal = deal
        self.history_queryset = self.deal.activity.history.all()[:max_items]
        self.history_queue = deque(self.history_queryset)

    def __iter__(self):
        inital_activity = self.history_queue.popleft()
        self.earlier_deal = Deal.from_activity(inital_activity)
        self.later_deal = None

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
        try:
            activity = self.history_queue.popleft()
        except IndexError:
            raise StopIteration
        else:
            self.earlier_deal = Deal.from_activity(activity)

        changes = self.compare_deals()

        return self.later_deal, changes
