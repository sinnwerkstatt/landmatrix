from django.contrib.auth.models import AnonymousUser, User, Group, Permission
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import Http404

from grid.views import AddDealView, ChangeDealView, DeleteDealView, RecoverDealView, DealDetailView
from editor.views import ManageAddsView, ManageUpdatesView, ManageDeletesView, ManageMyDealsView, \
    ApproveActivityChangeView, ApproveActivityDeleteView
from landmatrix.models import HistoricalActivity, Activity

class TestAddDeal(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
    ]

    def setUp(self):
        self.users = {
            'reporter': User.objects.get(username='reporter'),
            'editor': User.objects.get(username='editor'),
            'administrator': User.objects.get(username='administrator'),
        }
        self.groups = {
            'reporter': Group.objects.get(name='Reporters'),
            'editor': Group.objects.get(name='Editors'),
            'administrator': Group.objects.get(name='Administrators'),
        }
        self.factory = RequestFactory()

        # Create group permissions
        # This not possible in fixtures, because permissions and content types are created on run-time
        perm_review_activity = Permission.objects.get(codename='review_activity')
        self.groups['editor'].permissions.add(perm_review_activity)
        perm_add_activity = Permission.objects.get(codename='add_activity')
        perm_change_activity = Permission.objects.get(codename='change_activity')
        self.groups['administrator'].permissions.add(perm_review_activity)
        self.groups['administrator'].permissions.add(perm_add_activity)
        self.groups['administrator'].permissions.add(perm_change_activity)

    def test_add_deal_as_reporter(self):
        # Add deal as reporter
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test add deal",
        }
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = AddDealView.as_view()(request)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.pending().latest()

        # Check if deal appears in my deals section of reporter
        request = self.factory.get(reverse('manage_my_deals'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageMyDealsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)

        # Check if deal NOT appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 0)

        # Check if deal appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)

    def test_add_deal_as_editor(self):
        # Add deal as editor
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test add deal",
        }
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = AddDealView.as_view()(request)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.pending().latest()

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['editor'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)

    def test_add_deal_as_administrator(self):
        # Add deal as administrator
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test add deal",
        }
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = AddDealView.as_view()(request)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.active().latest()

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)


class TestChangeDeal(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        self.users = {
            'reporter': User.objects.get(username='reporter'),
            'editor': User.objects.get(username='editor'),
            'administrator': User.objects.get(username='administrator'),
        }
        self.groups = {
            'reporter': Group.objects.get(name='Reporters'),
            'editor': Group.objects.get(name='Editors'),
            'administrator': Group.objects.get(name='Administrators'),
        }
        self.factory = RequestFactory()

        # Create group permissions
        # This not possible in fixtures, because permissions and content types are created on run-time
        perm_review_activity = Permission.objects.get(codename='review_activity')
        self.groups['editor'].permissions.add(perm_review_activity)
        perm_add_activity = Permission.objects.get(codename='add_activity')
        perm_change_activity = Permission.objects.get(codename='change_activity')
        perm_delete_activity = Permission.objects.get(codename='delete_activity')
        self.groups['administrator'].permissions.add(perm_review_activity)
        self.groups['administrator'].permissions.add(perm_add_activity)
        self.groups['administrator'].permissions.add(perm_change_activity)
        self.groups['administrator'].permissions.add(perm_delete_activity)

    def test_change_deal_as_reporter(self):
        # Change deal as reporter
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test change deal",
        }
        request = self.factory.post(reverse('change_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ChangeDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.pending().latest()

        # Check if deal appears in my deals section of reporter
        request = self.factory.get(reverse('manage_my_deals'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageMyDealsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)

        # Check if deal NOT appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 0)

        # Check if deal appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)

    def test_change_deal_as_editor(self):
        # Change deal as editor
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test change deal",
        }
        request = self.factory.post(reverse('change_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ChangeDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.pending().latest()

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['editor'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)

    def test_change_deal_as_administrator(self):
        # Change deal as administrator
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Location
            "location-TOTAL_FORMS": 1,
            "location-INITIAL_FORMS": 0,
            "location-MIN_NUM_FORMS": 1,
            "location-MAX_NUM_FORMS": 1000,
            "location-0-level_of_accuracy": "Exact location",
            "location-0-location": "Berlin, Deutschland",
            "location-0-location-map": "Berlin, Deutschland",
            "location-0-point_lat": 52.52000659999999,
            "location-0-point_lon": 13.404953999999975,
            "location-0-target_country": 276,
            # Contract
            "contract-TOTAL_FORMS": 0,
            "contract-INITIAL_FORMS": 0,
            "contract-MIN_NUM_FORMS": 0,
            "contract-MAX_NUM_FORMS": 0,
            # Data source
            "data_source-TOTAL_FORMS": 0,
            "data_source-INITIAL_FORMS": 0,
            "data_source-MIN_NUM_FORMS": 0,
            "data_source-MAX_NUM_FORMS": 0,
            # Action comment
            "tg_action_comment": "Test change deal",
        }
        request = self.factory.post(reverse('change_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ChangeDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.active().latest()

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 200)


class TestDeleteDeal(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        self.users = {
            'reporter': User.objects.get(username='reporter'),
            'editor': User.objects.get(username='editor'),
            'administrator': User.objects.get(username='administrator'),
        }
        self.groups = {
            'reporter': Group.objects.get(name='Reporters'),
            'editor': Group.objects.get(name='Editors'),
            'administrator': Group.objects.get(name='Administrators'),
        }
        self.factory = RequestFactory()

        # Create group permissions
        # This not possible in fixtures, because permissions and content types are created on run-time
        perm_review_activity = Permission.objects.get(codename='review_activity')
        self.groups['editor'].permissions.add(perm_review_activity)
        perm_add_activity = Permission.objects.get(codename='add_activity')
        perm_change_activity = Permission.objects.get(codename='change_activity')
        perm_delete_activity = Permission.objects.get(codename='delete_activity')
        self.groups['administrator'].permissions.add(perm_review_activity)
        self.groups['administrator'].permissions.add(perm_add_activity)
        self.groups['administrator'].permissions.add(perm_change_activity)
        self.groups['administrator'].permissions.add(perm_delete_activity)

    def test_delete_deal_as_reporter(self):
        # Delete deal as reporter
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal",
        }
        request = self.factory.post(reverse('delete_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = DeleteDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.to_delete().latest()

        # Check if deal appears in my deals section of reporter
        request = self.factory.get(reverse('manage_my_deals'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageMyDealsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)

        # Check if deal NOT appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 0)

        # Check if deal appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_delete_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['reporter'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_delete_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            pass
        else:
            self.fail("Deal still exists after deletion")

    def test_delete_deal_as_editor(self):
        # Delete deal as editor
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal",
        }
        request = self.factory.post(reverse('delete_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = DeleteDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.to_delete().latest()

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        activities = list(response.context_data['activities'])
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['id'], activity.id)
        self.assertEqual(activities[0]['user'], self.users['editor'].username)

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_delete_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            pass
        else:
            self.fail("Deal still exists after deletion")

    def test_delete_deal_as_administrator(self):
        # Delete deal as administrator
        activity = HistoricalActivity.objects.active().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal",
        }
        request = self.factory.post(reverse('delete_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = DeleteDealView.as_view()(request, deal_id=activity.activity_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302)

        activity = HistoricalActivity.objects.deleted().latest()

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            pass
        else:
            self.fail("Deal still exists after deletion")

    def test_recover_deal_as_editor(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal",
        }
        request = self.factory.post(reverse('recover_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = RecoverDealView.as_view()(request, deal_id=activity.activity_identifier)
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            pass
        else:
            self.fail("Deal recovered although editors shouldn't be able to recover")

    def test_recover_deal_as_administrator(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal",
        }
        request = self.factory.post(reverse('recover_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = RecoverDealView.as_view()(request, deal_id=activity.activity_identifier)
        self.assertEqual(response.status_code, 302)

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            self.fail("Deal still deleted after recovering")
        else:
            pass