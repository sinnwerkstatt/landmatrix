from django.test import TestCase
from django.utils import timezone

from .models import NotificationEmail


class NotificationEmailTestCase(TestCase):

    sent_email = NotificationEmail(sent_on=timezone.now(),
                                   sent_status=NotificationEmail.STATUS_SENT)
    new_email = NotificationEmail(sent_on=None,
                                  sent_status=NotificationEmail.STATUS_NEW)

    def test_is_sent_when_sent(self):
        self.assertTrue(self.sent_email.is_sent)

    def test_is_sent_when_not_sent(self):
        self.assertFalse(self.new_email.is_sent)

    def test_is_new_when_new(self):
        self.assertTrue(self.new_email.is_new)

    def test_is_new_when_sent(self):
        self.assertFalse(self.sent_email.is_new)
