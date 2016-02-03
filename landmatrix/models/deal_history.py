from django.core.exceptions import ObjectDoesNotExist

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.deal import Deal, aggregate_activity_attributes

from collections import OrderedDict
from datetime import datetime, time, tzinfo

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealHistoryItem(Deal):

    date = None
    use_rounded_dates = True

    @classmethod
    def from_activity_with_date(cls, activity, date):
        cls.date = date
        deal = cls()
        # if not isinstance(activity, Activity):
        #     activity = Activity.objects.get(activity.id)
        deal._set_activity(activity)
        cls.date = None
        return deal

    @classmethod
    def get_history_for(cls, deal):
        tmp_use_rounded_dates = cls.use_rounded_dates
        cls.use_rounded_dates = False
        my_deal = cls.from_activity_with_date(deal.activity, datetime.now())
        cls.use_rounded_dates = tmp_use_rounded_dates
        return my_deal.get_history()

    def get_activity_attributes(self):
        attributes = ActivityAttributeGroup.objects.filter(fk_activity_id=self.activity.id)

        if self.date:
            attributes = [a.history.as_of(self.date) for a in attributes if existed_at_date(a, self.date)]

        attributes_list = [a.attributes for a in attributes]
        return aggregate_activity_attributes(attributes_list, {})

    def get_user(self):
        return self.activity.changed_by

    def get_history(self):
        return OrderedDict(reversed(sorted(self._activity_history(), key=lambda item: item[0])))

    def _activity_history(self):
        date_and_activity = []
        for activity in list(self.activity.history.filter(
                activity_identifier=self.activity.activity_identifier
        ).order_by('history_date')):
            date_and_activity.append((activity.history_date, DealHistoryItem.from_activity(activity)))

        for date in self.get_change_dates():
            try:
                historical_activity = self.activity.history.as_of(date)
                date_and_activity.append(
                        (date,
                         DealHistoryItem.from_activity_with_date(
                                 historical_activity, date))
                )
            except ObjectDoesNotExist:
                pass

        return sorted(date_and_activity, key=lambda entry: entry[0])

    def get_change_dates(self):
        attributes_history_dates = [
            item[0]
            for item in ActivityAttributeGroup.history.filter(fk_activity_id=self.activity.id).values_list('history_date')
        ]

        if not self.use_rounded_dates:
            return attributes_history_dates

        return _unique_rounded_dates(attributes_history_dates)


def _unique_rounded_dates(dates):
    return sorted(list(set([_rounded_date(d) for d in dates])))


def _rounded_date(d):
    from django.utils import timezone
    return datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, tzinfo=timezone.now().tzinfo)


def existed_at_date(a, date):
    try:
        a.history.as_of(date)
        return True
    except ObjectDoesNotExist:
        return False

