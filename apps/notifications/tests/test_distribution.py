from django.core import mail
from django.test import RequestFactory, TestCase

from apps.landmatrix.models import HistoricalActivity
from apps.notifications.distribution import *
from apps.public_comments.models import ThreadedComment


class DistributionTestCase(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        user = get_user_model().objects.get(username='reporter')
        self.activity = HistoricalActivity.objects.get(id=10)
        self.comment = ThreadedComment.objects.create(user=user,
                                                      comment='comment',
                                                      content_object=self.activity,
                                                      site_id=1)
        self.parent_comment = ThreadedComment.objects.create(user_email='reporter-2@example.com',
                                                             comment='parent comment',
                                                             content_object=self.activity,
                                                             site_id=1)
        self.request = RequestFactory()

    def test_get_recipients_for_comment_on_activity(self):
        recipients = get_recipients_for_comment_on_activity(self.comment, self.activity)
        expected = {'administrator-myanmar@example.com', 'editor-asia@example.com',
                    'administrator-asia@example.com', 'editor-myanmar@example.com'}
        self.assertEqual(expected, recipients)

    def test_get_recipients_for_comment_on_activity_with_parent(self):
        user = get_user_model().objects.get(username='reporter-2')
        self.parent_comment.user = user
        self.parent_comment.save()
        self.comment.parent = self.parent_comment
        self.comment.save()
        recipients = get_recipients_for_comment_on_activity(self.comment, self.activity)
        expected = {'editor-myanmar@example.com', 'editor-asia@example.com', 'reporter2@example.com',
                    'administrator-asia@example.com', 'administrator-myanmar@example.com'}
        self.assertEqual(expected, recipients)

    def test_get_recipients_for_comment_on_activity_with_parent_email(self):
        self.comment.parent = self.parent_comment
        self.comment.save()
        recipients = get_recipients_for_comment_on_activity(self.comment, self.activity)
        expected = {'administrator-myanmar@example.com', 'editor-asia@example.com', 'administrator-asia@example.com',
                    'reporter-2@example.com', 'editor-myanmar@example.com'}
        self.assertEqual(expected, recipients)

    def test_send_notifications_for_comment_on_activity(self):
        send_notifications_for_comment_on_activity(self.comment, self.request, self.activity)
        queryset = NotificationEmail.objects.all()
        self.assertGreater(queryset.count(), 0)
        self.assertGreater(len(mail.outbox), 0)
