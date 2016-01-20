from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from landmatrix.models.activity import Activity
from landmatrix.models.investor import Investor, InvestorActivityInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestDealDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.history_ids = []

    def test_how_to_call_a_view_that_works(self):
        response = self._get_url_following_redirects('/en/global_app/all')
        self.assertEqual(200, response.status_code)

    def test_view_nonexistent_activity_history_id(self):
        with self.assertRaises(ObjectDoesNotExist):
            self._get_url_following_redirects('/global_app/compare/1/2/')

    def test_view_invalid_parameter(self):
        with self.assertRaises(RuntimeError):
            self._get_url_following_redirects('/global_app/compare/1x2/')

    def test_history_gets_called_with_activity_history_ids(self):
        self._create_activity_history()
        response = self._get_url_following_redirects(
                '/global_app/compare/%i/%i/' % (self.history_ids[0], self.history_ids[1])
        )
        self.assertEqual(200, response.status_code)

    def test_history_with_activity_history_ids_content(self):
        self._create_activity_history()
        response = self._get_url_following_redirects(
                '/global_app/compare/%i/%i/' % (self.history_ids[0], self.history_ids[1])
        )
        # nothing to test here really unless you got to the trouble of creating activities with data

    def test_view_nonexistent_activity_identifier_and_timestamp(self):
        with self.assertRaises(ObjectDoesNotExist):
            self._get_url_following_redirects('/global_app/compare/1_2/')

    def test_view_with_activity_identifier_and_timestamp(self):
        self._create_activity_history()
        activity = Activity.history.get(history_id=self.history_ids[0])
        activity_identifier = activity.activity_identifier
        timestamp = date_string_to_timestamp(activity.history_date)
        try:
            response = self._get_url_following_redirects('/global_app/compare/%i_%s/' % (activity_identifier, timestamp))
        except NotImplementedError:
            self.skipTest('nyi, tbd, brb')

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response

    def _create_activity_history(self, act_id=1):
        act = Activity(activity_identifier=act_id, availability=1, fk_status_id=2)
        act.save()
        act.availability = 2
        act.save()
        inv = Investor(investor_identifier=1, fk_status_id=2)
        inv.save()
        link = InvestorActivityInvolvement(fk_investor=inv, fk_activity=act, fk_status_id=2)
        link.save()
        self.history_ids = [a.history_id for a in act.history.all()]
        self.assertEqual(2, len(self.history_ids))


def random_recognizable_number():
    from random import randint
    return randint(1000000000, 2147483646)

def date_string_to_timestamp(date):
    from datetime import datetime
    from time import mktime
    return date.timestamp()
    timestamp = mktime(datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").timetuple())
    return timestamp