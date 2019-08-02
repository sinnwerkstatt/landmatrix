from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import QueryDict
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.translation import LANGUAGE_SESSION_KEY

from landmatrix.views import SwitchLanguageView


class SwitchLanguageViewTestCase(TestCase):

    fixtures = [
        'languages'
    ]

    def setUp(self):
        self.factory = RequestFactory()

    def test_with_valid_language(self):
        request = self.factory.get(reverse('switch_language', kwargs={'language': 'en'}))
        request.GET = QueryDict('next=/')
        request.session = {}
        request._messages = FallbackStorage(request)
        response = SwitchLanguageView.as_view()(request, language='en')
        self.assertEqual(302, response.status_code)

        self.assertEqual('en', request.session[LANGUAGE_SESSION_KEY])
        self.assertEqual('en', request.session['django_language'])
        self.assertEqual('en', request.LANGUAGE_CODE)

    def test_with_invalid_language(self):
        request = self.factory.get(reverse('switch_language', kwargs={'language': 'xx'}))
        request.GET = QueryDict('next=/')
        request.session = {}
        request._messages = FallbackStorage(request)
        response = SwitchLanguageView.as_view()(request, language='xx')
        self.assertEqual(302, response.status_code)

        messages = list(request._messages)
        self.assertGreater(len(messages), 0)
        self.assertEqual('The language "xx" is not supported', messages[-1].message)
