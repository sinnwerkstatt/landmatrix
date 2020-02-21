import os
import re

from django.core.management import call_command
from django.core.management.base import OutputWrapper
from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from django.conf import settings
import importlib

from apps.api.elasticsearch import ElasticSearch, es_save
from apps.landmatrix.tests.mixins import ElasticSearchFixtureMixin
from apps.wagtailcms.models import WagtailRootPage


class UrlsTest(ElasticSearchFixtureMixin, TestCase):

    inv_fixtures = [{"id": 1, "investor_identifier": 1}]

    default_kwargs = {
        "app_label": "sites",
        "content_type_id": "1",
        "object_id": "1",
        "id": "1",
        "activation_key": "1",
        "uidb64": "1",
        "token": "1-1",
    }
    skip_regex = r"^.*_pdf$"

    def setUp(self):
        super().setUp()
        WagtailRootPage.objects.create(title="Root", path="/", depth=0)

    def assert_urls_available(
        self,
        allowed_http_codes=(200, 302, 405),
        credentials={},
        default_kwargs={},
        quiet=True,
    ):
        """
        Test all pattern in root urlconf and included ones.
        Do GET requests only.
        A pattern is skipped if any of the conditions applies:
            - pattern has no name in urlconf
            - pattern expects any positinal parameters
            - pattern expects keyword parameters that are not specified in @default_kwargs
        If response code is not in @allowed_http_codes, fail the test.
        if @credentials dict is specified (e.g. username and password),
            login before run tests.
        If @logout_url is specified, then check if we accidentally logged out
            the client while testing, and login again
        Specify @default_kwargs to be used for patterns that expect keyword parameters,
            e.g. if you specify default_kwargs={'username': 'testuser'}, then
            for pattern url(r'^accounts/(?P<username>[\.\w-]+)/$'
            the url /accounts/testuser/ will be tested.
        If @quiet=False, print all the urls checked. If status code of the response is not 200,
            print the status code.
        """
        module = importlib.import_module(settings.ROOT_URLCONF)
        if credentials:
            self.client.login(**credentials)

        def check_urls(urlpatterns, prefix=""):
            for pattern in urlpatterns:
                if hasattr(pattern, "url_patterns"):
                    # this is an included urlconf
                    new_prefix = prefix
                    if pattern.namespace:
                        new_prefix = (
                            prefix + (":" if prefix else "") + pattern.namespace
                        )
                    check_urls(pattern.url_patterns, prefix=new_prefix)
                params = {}
                skip = False
                regex = pattern.pattern.regex
                if regex.groups > 0:
                    # the url expects parameters
                    # use default_kwargs supplied
                    if regex.groups > len(regex.groupindex.keys()) or set(
                        regex.groupindex.keys()
                    ) - set(default_kwargs.keys()):
                        # there are positional parameters OR
                        # keyword parameters that are not supplied in default_kwargs
                        # so we skip the url
                        skip = True
                    else:
                        for key in set(default_kwargs.keys()) & set(
                            regex.groupindex.keys()
                        ):
                            params[key] = default_kwargs[key]
                if hasattr(pattern.pattern, "name") and pattern.pattern.name:
                    name = pattern.pattern.name
                else:
                    # if pattern has no name, skip it
                    skip = True
                    name = ""
                fullname = (prefix + ":" + name) if prefix else name
                if re.match(self.skip_regex, fullname):
                    skip = True
                if not skip:
                    url = reverse(fullname, kwargs=params)
                    # If Schema defined, use example values as GET parameters
                    data = {}
                    view = resolve(url)
                    if hasattr(view.func, "view_class") and hasattr(
                        view.func.view_class, "schema"
                    ):
                        schema = view.func.view_class.schema
                        if hasattr(schema, "_fields"):
                            data = dict(
                                (
                                    (f.name, f.example)
                                    for f in schema._fields
                                    if f.example
                                )
                            )
                    response = self.client.get(url, data=data)
                    self.assertIn(
                        response.status_code,
                        allowed_http_codes,
                        msg=f"URL {url} returned status code {response.status_code}",
                    )
                    # print status code if it is not 200
                    status = (
                        ""
                        if response.status_code == 200
                        else str(response.status_code) + " "
                    )
                    if not quiet:
                        print(status + url)
                    if "logout" in url and credentials:
                        # if we just tested logout, then login again
                        self.client.login(**credentials)
                else:
                    if not quiet:
                        print("SKIP " + regex.pattern + " " + fullname)

        check_urls(module.urlpatterns)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        """
        Test all URLs as superuser
        :param self:
        :return:
        """
        credentials = {"username": "superuser", "password": "test"}
        self.assert_urls_available(
            credentials=credentials, default_kwargs=self.default_kwargs
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        """
        Test all URLs as administrator
        :param self:
        :return:
        """
        credentials = {"username": "administrator", "password": "test"}
        self.assert_urls_available(
            allowed_http_codes=(200, 302, 403, 405),
            credentials=credentials,
            default_kwargs=self.default_kwargs,
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        """
        Test all URLs as administrator
        :param self:
        :return:
        """
        credentials = {"username": "editor", "password": "test"}
        self.assert_urls_available(
            allowed_http_codes=(200, 302, 403, 405),
            credentials=credentials,
            default_kwargs=self.default_kwargs,
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        """
        Test all URLs as administrator
        :param self:
        :return:
        """
        credentials = {"username": "reporter", "password": "test"}
        self.assert_urls_available(
            allowed_http_codes=(200, 302, 403, 405),
            credentials=credentials,
            default_kwargs=self.default_kwargs,
        )
