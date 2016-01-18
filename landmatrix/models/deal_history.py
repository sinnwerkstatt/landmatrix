from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.deal import Deal, aggregate_activity_attributes

from collections import OrderedDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealHistoryItem(Deal):

    date = None
    use_rounded_dates = True

    @classmethod
    def from_activity_with_date(cls, activity, date):
        cls.date = date
        deal = super().from_activity(activity)
        cls.date = None
        return deal

    def get_activity_attributes(self):
        attributes = ActivityAttributeGroup.objects.filter(fk_activity=self.activity)

        if self.date:
            attributes = [a.history.as_of(DealHistoryItem.date) for a in attributes]

        attributes_list = [a.attributes for a in attributes]
        return aggregate_activity_attributes(attributes_list, {})

    def get_user(self):
        return self.activity.changed_by

    def get_history(self):
        return OrderedDict(sorted(self._activity_history(), key=lambda item: item[0]))

    def _activity_history(self):
        date_and_activity = []
        for activity in list(self.activity.history.filter(
                activity_identifier=self.activity.activity_identifier
        ).order_by('history_date')):
            date_and_activity.append((activity.history_date, DealHistoryItem.from_activity(activity)))

        for date in self.get_change_dates():
            date_and_activity.append((date, DealHistoryItem.from_activity_with_date(self.activity.history.as_of(date), date)))

        return date_and_activity

    def get_change_dates(self):
        attributes_history_dates = [
            item[0]
            for item in ActivityAttributeGroup.history.filter(fk_activity_id=self.activity.id).values_list('history_date')
        ]

        if not self.use_rounded_dates:
            return attributes_history_dates

        return _unique_rounded_dates(attributes_history_dates)


def _unique_rounded_dates(dates):
    from datetime import datetime
    return sorted(list(set([datetime(d.year, d.month, d.day, d.hour, d.minute, d.second) for d in dates])))


