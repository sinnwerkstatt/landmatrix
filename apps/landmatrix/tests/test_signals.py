from django.test import TestCase
from django.urls import reverse
from django.utils.datastructures import MultiValueDict


class SignalsTestCase(TestCase):
    def test_create_userregionalinfo(self):
        data = MultiValueDict(
            {
                "username": ["username"],
                "password1": ["password"],
                "password2": ["password"],
                "first_name": ["first_name"],
                "last_name": ["last_name"],
                "email": ["root@localhost.com"],
                "information": ["information"],
                "g-recaptcha-response": ["g-recaptcha-response"],
            }
        )
        response = self.client.post(reverse("django_registration_register"), data)
        user = response.context.get("user")
        self.assertEqual(True, hasattr(user, "userregionalinfo"))
        self.assertEqual(
            {"Reporters"}, set(user.groups.all().values_list("name", flat=True))
        )
        self.assertEqual("information", user.userregionalinfo.information)
