import traceback

from django.core.exceptions import ObjectDoesNotExist

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.deal import Deal

from collections import OrderedDict
from datetime import datetime, time, tzinfo
from dateutil.tz import tzlocal



class DealHistoryItem(Deal):
    """Deprecated: Will be delete soon"""

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
        my_deal = cls.from_activity_with_date(deal.activity, datetime.now(tzlocal()))
        cls.use_rounded_dates = tmp_use_rounded_dates
        return my_deal.get_history()

    def get_activity_attributes(self):
        if self.date:
            return dict(ActivityAttribute.history.filter(history_date__lte=self.date, fk_activity_id=self.activity.id).values_list('name', 'value'))
        else:
            return dict(ActivityAttribute.objects.filter(fk_activity_id=self.activity.id).values_list('name', 'value'))
        return attributes

    def get_user(self):
        return self.activity.changed_by

    def get_history(self):
        return OrderedDict(reversed(sorted(self._activity_history(), key=lambda item: item[0])))

    def _activity_history(self):
        date_and_activity = []
        for activity in list(self.activity.history.filter(
                activity_identifier=self.activity.activity_identifier
        ).order_by('history_date')):
            date_and_activity.append((activity.history_date.timestamp(), DealHistoryItem.from_activity(activity)))

        for date in self.get_change_dates():
            try:
                historical_activity = self.activity.history.as_of(date)
                date_and_activity.append(
                        (date.timestamp(),
                         DealHistoryItem.from_activity_with_date(
                                 historical_activity, date))
                )
            except ObjectDoesNotExist:
                pass

        return sorted(date_and_activity, key=lambda entry: entry[0])

    def get_change_dates(self):
        attrs = [a[0] for a in ActivityAttribute.history.filter(fk_activity_id=self.activity.id).order_by('history_date').values_list('history_date')]
        #if not self.use_rounded_dates:
        #    from django.utils import timezone
        #    attrs = [datetime(aa.year, aa.month, aa.day, aa.hour, aa.minute, aa.second,
        #        tzinfo=timezone.now().tzinfo) for aa in attrs]
        return attrs