from django.core import mail
from django.test import TestCase
from django.utils import timezone

from apps.notifications.exceptions import AlreadySentError, NotificationError
from apps.notifications.models import NotificationEmail, NotificationEmailManager


class NotificationEmailManagerTestCase(TestCase):
    def test(self):
        manager = NotificationEmailManager()
        manager.send(to="report@example.com", subject="NEW")
        self.assertGreater(NotificationEmail.objects.count(), 0)
        self.assertGreater(len(mail.outbox), 0)


class NotificationEmailTestCase(TestCase):
    def setUp(self):
        self.context = {
            "comment": {
                "name": "name",
                "title": "title",
                "comment": "comment",
                "content_object": {"activity_identifier": 1},
            }
        }
        self.email_new = NotificationEmail.objects.create(
            to="to@example.com",
            cc="cc@example.com",
            bcc="bcc@example.com",
            reply_to="reply_to@example.com",
            subject="NEW",
            sent_status=NotificationEmail.STATUS_NEW,
            template_name="comment_posted",
            context=self.context,
        )
        self.email_sent = NotificationEmail.objects.create(
            to="reporter@example.com",
            subject="SENT",
            sent_status=NotificationEmail.STATUS_NEW,
            template_name="comment_posted",
            context=self.context,
        )
        self.email_sent.sent_status = NotificationEmail.STATUS_SENT
        self.email_sent.sent_on = timezone.now()
        self.email_sent.save()

    def test_render_template(self):
        self.email_new.render_template("comment_posted", self.context)
        self.assertGreater(len(self.email_new.body_text), 0)
        self.assertGreater(len(self.email_new.body_html), 0)

    def test_render_template_without_new(self):
        with self.assertRaises(NotificationError):
            self.email_sent.render_template("comment_posted", self.context)

    def test_is_sent_with_sent(self):
        self.assertEqual(True, self.email_sent.is_sent)

    def test_is_sent_without_sent(self):
        self.assertEqual(False, self.email_new.is_sent)

    def test_is_new_with_new(self):
        self.assertEqual(True, self.email_new.is_new)

    def test_is_new_without_new(self):
        self.assertEqual(False, self.email_sent.is_new)

    def test_send_with_html(self):
        self.email_new.body_text = "body_text"
        self.email_new.body_html = "body_html"
        self.email_new.send()
        self.assertEqual(NotificationEmail.STATUS_SENT, self.email_new.sent_status)
        self.assertIsNotNone(self.email_new.sent_on)
        self.assertEqual("", self.email_new.sent_exception)
        self.assertGreater(len(mail.outbox), 0)

    def test_send_without_html(self):
        self.email_new.body_text = "body_text"
        self.email_new.send()
        self.assertEqual(NotificationEmail.STATUS_SENT, self.email_new.sent_status)
        self.assertIsNotNone(self.email_new.sent_on)
        self.assertEqual("", self.email_new.sent_exception)
        self.assertGreater(len(mail.outbox), 0)

    def test_send_with_sent(self):
        with self.assertRaises(AlreadySentError):
            self.email_sent.send()
