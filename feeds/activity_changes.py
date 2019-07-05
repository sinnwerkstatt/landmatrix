from landmatrix.models import HistoricalActivity


class ActivityChangesList:
    """
    An iterator to go over activity history.
    """

    def __init__(self, activity_identifier, max_items=100):
        self.activity_identifier = activity_identifier
        queryset = HistoricalActivity.objects.filter(
            activity_identifier=self.activity_identifier)
        queryset = queryset.order_by('-history_date')[:max_items]
        self.history = list(queryset)

    def __iter__(self):
        self.index = 1  # index tracks the earlier activity, so off by 1
        try:
            self.later_activity = self.history[self.index - 1]
        except IndexError:
            self.later_activity = None

        try:
            self.earlier_activity = self.history[self.index]
        except IndexError:
            self.earlier_activity = None

        return self

    def compare_deals(self):
        """
        Returns a list of (group_id, key, later_value, earlier_value) tuples.
        """
        if not self.later_activity:
            changes = []
        else:
            changes = self.later_activity.compare_attributes_to(
                self.earlier_activity)

            if self.earlier_activity:
                stakeholder = self.earlier_activity.operational_stakeholder
            else:
                stakeholder = None
            if self.later_activity.operational_stakeholder != stakeholder:
                change = (
                    None,
                    'operational_stakeholder',
                    self.later_activity.operational_stakeholder,
                    stakeholder,
                )
                changes.append(change)

        return changes

    def __next__(self):
        self.index += 1

        self.later_activity = self.earlier_activity
        try:
            self.earlier_activity = self.history[self.index]
        except IndexError:
            self.earlier_activity = None

        if self.later_activity is None:
            raise StopIteration

        changes = self.compare_deals()

        return self.later_activity.history_date, self.later_activity, changes
