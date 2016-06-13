from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.deal import Deal
from landmatrix.models.deal_history import DealHistoryItem
from landmatrix.models.investor import InvestorActivityInvolvement, Investor
from landmatrix.models.language import Language
from landmatrix.tests.with_status import WithStatus

from django.utils import timezone

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestDealHistory(WithStatus):

    def setUp(self):
        WithStatus.setUp(self)
        Language(english_name='English', local_name='English', locale='en').save()
        self.language = Language.objects.last()
        DealHistoryItem.use_rounded_dates = False

    def test_get_history_single(self):
        activity = _create_activity(1)
        deal = DealHistoryItem.from_activity(activity)
        self.assertEqual(1, len(deal.get_history()))
        self.assertEqual(deal, list(deal.get_history().values())[0])

    def test_get_history_activity_changed(self):
        deal = _create_deal_history()
        self.assertEqual(2, len(deal.get_history()))
        self.assertEqual(deal, list(deal.get_history().values())[0])

    def test_get_history_activity_ordered_by_date(self):
        deal = _create_deal_history()
        history = deal.get_history()
        history_item = history.popitem(last=True)
        for i in range(0, len(history)):
            next_item = history.popitem()
            self.assertGreater(next_item[0], history_item[0])
            history_item = next_item

        self.assertEqual(deal, list(deal.get_history().values())[0])

    def test_get_history_with_changed_attributes_returns_more_than_one_state(self):
        activity = self._create_activity_with_changed_attributes()
        deal = DealHistoryItem.from_activity(activity)
        self.assertGreater(len(deal.get_history()), 1)

    def test_history_with_changed_attributes_contains_correct_attributes(self):
        activity = self._create_activity_with_changed_attributes()
        deal = DealHistoryItem.from_activity(activity)
        history = deal.get_history()
        history_latest = history.popitem(last=True)
        history_older = history.popitem(last=True)
        self.assertEqual('blubb', history_latest[1].attributes['blah'])
        self.assertEqual('blunb', history_older[1].attributes['blah'])

    def _create_activity_with_changed_attributes(self):
        act = _create_activity(1)
        aa = ActivityAttribute.objects.create(
                fk_activity=act,
                fk_language=self.language,
                name='blah',
                value='blunb'
        )
        aa.value = 'blubb'  # oops, these darn typos!
        aa.save()
        return activity


def _create_deal_history():
    activity = _create_activity_with_history()
    deal = DealHistoryItem.from_activity(activity)
    return deal


def _create_activity_with_history(act_id=1):
    activity = _create_activity(act_id)
    activity.availability = 0.6
    activity.save()
    return activity


def _create_activity(act_id):
    act = Activity.objects.create(
        activity_identifier=act_id,
        availability=0.5,
        fully_updated=timezone.now(),
        fk_status_id=2
    )
    inve = Investor.objects.create(
        investor_identifier=1,
        name='test investor',
        classification=10,
        fk_status_id=2
    )
    invo = InvestorActivityInvolvement.objects.create(
        fk_activity=Activity.objects.last(),
        fk_investor=Investor.objects.last(),
        fk_status_id=2,
        percentage=100
    )
    return act


