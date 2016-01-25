from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import User

from editor.models import UserRegionalInfo
from landmatrix.models.country import Country
from landmatrix.models.region import Region

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestEditorView(TestCase):

    NORMAL_USER = 'normal_user'
    NORMAL_PASSWORD = 'blah'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.NORMAL_USER, password=self.NORMAL_PASSWORD)

    def test_user_not_logged_in_redirects_to_login_page(self):
        url, response = self._get_url_following_redirects('/editor')
        self.assertEqual(200, response.status_code)
        self.assertIn(settings.LOGIN_URL, url)

    def test_wrong_user_login(self):
        self.assertFalse(self.client.login(username='this user does not exist', password='wrong password'))

    def test_correct_user_login(self):
        self.assertTrue(self.client.login(username=self.NORMAL_USER, password=self.NORMAL_PASSWORD))

    def test_editor_page_shows_when_logged_in(self):
        self.client.login(username=self.NORMAL_USER, password=self.NORMAL_PASSWORD)
        url, response = self._get_url_following_redirects('/editor')
        self.assertEqual(200, response.status_code)
        self.assertIn('/editor', url)

    def test_editor_page_contains_username(self):
        self.client.login(username=self.NORMAL_USER, password=self.NORMAL_PASSWORD)
        url, response = self._get_url_following_redirects('/editor')
        self.assertIn(self.NORMAL_USER, response.content.decode('utf-8'))

    def test_user_needs_region_info_filled(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.user.userregionalinfo

    def test_user_with_region_info(self):
        self._create_country_and_region()
        self._create_region_info()
        self.assertIn(self.country, self.user.userregionalinfo.country.all())
        self.assertIn(self.region, self.user.userregionalinfo.region.all())

    def _create_region_info(self):
        region_info = UserRegionalInfo(user=self.user)
        region_info.save()
        region_info.country.add(self.country)
        region_info.region.add(self.region)
        return region_info

    def _create_country_and_region(self):
        self.region = Region(name='Test Region', slug='test_region')
        self.region.save()
        self.country = Country(name='Test Country', fk_region=self.region)
        self.country.save()

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            url = response.url
            response = self.client.get(url)
        return url, response