from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin
from apps.notifications.models import NotificationEmail
from apps.public_comments.forms import PublicCommentForm


class SignalsTestCase(ActivitiesFixtureMixin, TestCase):

    act_fixtures = [{"id": 10, "activity_identifier": 1}]

    @override_settings(DEBUG=True)
    def test_handle_comment_on_activity_posted(self):
        data = MultiValueDict(
            {
                "name": ["name"],
                "email": ["reporter@example.com"],
                "url": ["https://example.com"],
                "comment": ["comment"],
                "g-recaptcha-response": ["g-recaptcha-response"],
            }
        )
        activity = HistoricalActivity.objects.get(id=10)
        form = PublicCommentForm(activity)
        data.update(form.generate_security_data())
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("comments-post-comment"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertGreater(NotificationEmail.objects.count(), 0)
        self.assertGreater(len(mail.outbox), 0)
