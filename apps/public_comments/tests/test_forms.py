from django.test import TestCase

from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin
from apps.public_comments.forms import EditCommentForm, PublicCommentForm


class PublicCommentFormTestCase(ActivitiesFixtureMixin, TestCase):

    act_fixtures = [{"id": 10, "activity_identifier": 1}]

    def setUp(self):
        super().setUp()
        self.activity = HistoricalActivity.objects.get(id=10)
        self.form = PublicCommentForm(self.activity)

    def test_init(self):
        self.assertNotIn("honeypot", self.form.fields.keys())

    def test_security_errors(self):
        self.form._errors = {
            "spam_protection": "spam_protection error",
            "timestamp": "timestamp error",
            "security_hash": "security_hash error",
            "comment": "comment error",
        }
        self.assertNotIn("other", self.form.security_errors().keys())


class EditCommentFormTestCase(ActivitiesFixtureMixin, TestCase):

    act_fixtures = [{"id": 10, "activity_identifier": 1}]

    def setUp(self):
        super().setUp()
        self.activity = HistoricalActivity.objects.get(id=10)
        self.form = EditCommentForm(self.activity)

    def test_init(self):
        self.assertEqual(True, self.form.fields["user_name"].widget.attrs["readonly"])
        self.assertEqual(True, self.form.fields["user_email"].widget.attrs["readonly"])
        self.assertEqual(True, self.form.fields["ip_address"].widget.attrs["readonly"])
