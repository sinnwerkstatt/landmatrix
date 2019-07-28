from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory


class MockRequestMixin:

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def mock_request(self, method, url, user, data=None):
        """
        Mock request
        :param method:
        :param url:
        :param data:
        :return:
        """
        request = getattr(self.factory, method)(url, data=data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # Editor without country/region
        if isinstance(user, str) and hasattr(self, 'users'):
            request.user = self.users[user]
        else:
            request.user = user
        return request
