from django.contrib.admin.sites import AdminSite
from django.core import mail
from django.test import RequestFactory, TestCase

from apps.notifications.admin import NotificationEmailAdmin
from apps.notifications.models import NotificationEmail


class NotificationEmailAdminTestCase(TestCase):
    def setUp(self):
        self.admin = NotificationEmailAdmin(
            model=NotificationEmail, admin_site=AdminSite()
        )
        self.request = RequestFactory()

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request))

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request))

    def test_resend_failed_emails(self):
        NotificationEmail.objects.create(
            to="reporter@example.com",
            subject="NEW",
            sent_status=NotificationEmail.STATUS_NEW,
        )
        NotificationEmail.objects.create(
            to="reporter@example.com",
            subject="ERROR",
            sent_status=NotificationEmail.STATUS_ERROR,
        )
        queryset = NotificationEmail.objects.all()
        self.admin.resend_failed_emails(self.request, queryset)
        self.assertEqual(
            {NotificationEmail.STATUS_SENT},
            set(queryset.values_list("sent_status", flat=True)),
        )
        self.assertGreater(len(mail.outbox), 0)
