from django.test import TestCase

from apps.grid.forms.public_user_information_form import PublicUserInformationForm


class PublicUserInformationFormTestCase(TestCase):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def setUp(self):
        self.data = {
            "tg_action_comment": "Test comment",
            "public_user_name": "Test user name",
            "public_user_email": "Test user email",
            "public_user_phone": "+123456789",
        }
        self.form = PublicUserInformationForm(data=self.data)

    def test_get_attributes(self):
        attrs = self.form.get_attributes()
        self.assertEqual({}, attrs)
