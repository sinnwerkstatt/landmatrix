from apps.grid.forms.deal_contract_form import DealContractForm
from apps.grid.forms.deal_data_source_form import DealDataSourceForm
from apps.grid.forms.deal_spatial_form import DealSpatialForm
from apps.grid.forms.investor_form import ExportInvestorForm
from apps.grid.forms.parent_investor_formset import InvestorVentureInvolvementForm
from apps.grid.utils import get_display_value
from apps.grid.views.utils import DEAL_FORMS
from apps.landmatrix.forms import ExportActivityForm
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin, InvestorsFixtureMixin, \
    InvestorActivityInvolvementsFixtureMixin, InvestorVentureInvolvementsFixtureMixin


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import csv
import zipfile
from io import BytesIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from openpyxl import load_workbook

from apps.api.elasticsearch import es_save


class ExportViewTestCase(TestCase,
                         ActivitiesFixtureMixin,
                         InvestorsFixtureMixin,
                         InvestorActivityInvolvementsFixtureMixin,
                         InvestorVentureInvolvementsFixtureMixin):

    act_fixtures = [
        {"id": 1, "attributes": {"intention": {"value": "Mining"}}}
    ]
    inv_fixtures = [
        {"id": 1},
        {"id": 2}
    ]
    act_inv_fixtures = {
        "1": "1"
    }
    inv_inv_fixtures = [
        {"fk_venture_id": "1", "fk_investor_id": "2"}
    ]

    deal_attributes = {}

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            "countries_and_regions",
            "users_and_groups",
            "status",
            "crops",
            "animals",
            "minerals",
            "currencies",
            # "investors",
            # "activities",
            # "activity_involvements",
            # "venture_involvements",
        ]
        for fixture in fixtures:
            call_command("loaddata", fixture, **{"verbosity": 0})
        cls.load_investor_fixtures()
        cls.load_activity_fixtures()
        cls.load_activity_involvement_fixtures()
        cls.load_investor_involvement_fixtures()
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

        cls.deal_attributes = cls._get_deal_attributes()
        cls.involvement_attributes = cls._get_involvement_attributes()
        cls.investor_attributes = cls._get_investor_attributes()

    def setUp(self):
        # Don't create fixtures for each test
        pass

    @classmethod
    def _get_deal_attributes(cls):
        """
        Get deal attributes for comparison
        :return:
        """
        deal_attributes = []

        # Get deal and calculcated attributes
        for act_attributes in cls.act_fixtures:
            attributes = {}
            attr_fixture = act_attributes.get("attributes")
            for form in DEAL_FORMS + [ExportActivityForm, ]:
                form = hasattr(form, "form") and form.form or form
                for i, (name, field) in enumerate(form.base_fields.items()):
                    if name.startswith("tg_") and not name.endswith("_comment"):
                        continue
                    if hasattr(form, "exclude_in_export") and \
                        name in form.exclude_in_export:
                        continue
                    if name in attr_fixture:
                        attr = attr_fixture.get(name)
                    elif name in cls.attr_fixtures_default:
                        attr = cls.attr_fixtures_default.get(name)
                    else:
                        field_class = type(field).__name__
                        if field_class not in cls.attr_fixtures_default_type:
                            field_class = "default"
                        attr = cls.attr_fixtures_default_type.get(field_class)
                    if callable(attr):
                        attr = attr(field, str(i))

                    # Get label
                    if form in (DealSpatialForm, DealDataSourceForm, DealContractForm):
                        label = f"{form.form_title} 1: {field.label}"
                    else:
                        label = field.label
                    value = get_display_value(field, [attr['value']], [attr])
                    attributes[label] = value
            deal_attributes.append(attributes)

        # Get operating company attributes
        for i, (act, inv) in enumerate(cls.act_inv_fixtures.items()):
            inv_attributes = list(filter(lambda i: str(i["id"]) == str(inv),
                                         cls.inv_fixtures))[0]
            inv_attributes_default = cls.inv_fixtures_default(inv_attributes)
            for name, field in ExportInvestorForm.base_fields.items():
                label = "%s: %s" % (_("Operating company"), field.label)
                if name in inv_attributes:
                    value = inv_attributes.get(name)
                else:
                    value = inv_attributes_default.get(name)
                value = get_display_value(field, [value])
                deal_attributes[i][label] = value

        return deal_attributes

    @classmethod
    def _get_involvement_attributes(cls):
        """
        Get involvement attributes for comparison
        :return:
        """
        involvement_attributes = []
        for inv_attributes in cls.inv_inv_fixtures:
            attributes = {}
            inv_attributes_default = cls.inv_fixtures_default(inv_attributes)
            for name, field in InvestorVentureInvolvementForm.base_fields.items():
                if name in inv_attributes:
                    value = inv_attributes.get(name)
                else:
                    value = inv_attributes_default.get(name)
                value = get_display_value(field, [value])
                attributes[field.label] = value
            involvement_attributes.append(attributes)
        return involvement_attributes

    @classmethod
    def _get_investor_attributes(cls):
        """
        Get investor attributes for comparison
        :return:
        """
        investor_attributes = []
        for inv_attributes in cls.inv_fixtures:
            attributes = {}
            inv_attributes_default = cls.inv_fixtures_default(inv_attributes)
            for j, (name, field) in enumerate(ExportInvestorForm.base_fields.items()):
                if name in inv_attributes:
                    value = inv_attributes.get(name)
                else:
                    value = inv_attributes_default.get(name)
                value = get_display_value(field, [value])
                attributes[field.label] = value
            investor_attributes.append(attributes)
        return investor_attributes

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def assert_deal_attributes_complete(self, deals):
        deal_attributes = dict(zip([c.value for c in next(deals)],
                                   [c.value for c in next(deals)]))
        for label, value in self.deal_attributes[0].items():
            if not value:
                continue
            self.assertIn(label, deal_attributes.keys())
            self.assertIn(value, deal_attributes[label])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def assert_involvements_complete(self, involvements):
        involvement_attributes = dict(zip([c.value for c in next(involvements)],
                                          [c.value for c in next(involvements)]))
        for label, value in self.involvement_attributes[0].items():
            if not value:
                continue
            self.assertIn(label, involvement_attributes.keys())
            self.assertIn(value, involvement_attributes[label])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def assert_investors_complete(self, investors):
        investor_attributes = dict(zip([c.value for c in next(investors)],
                                          [c.value for c in next(investors)]))
        for label, value in self.investor_attributes[0].items():
            if not value:
                continue
            self.assertIn(label, investor_attributes.keys())
            self.assertIn(value, investor_attributes[label])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def assert_xls_content(self, response):
        self.assertEqual("application/ms-excel", response["Content-Type"])
        wb = load_workbook(BytesIO(response.content), read_only=True)
        deals = wb["Deals"]
        self.assertGreater(len([row for row in deals.rows]), 1)
        self.assert_deal_attributes_complete(deals.rows)
        involvements = wb["Involvements"]
        self.assertGreater(len([row for row in involvements.rows]), 1)
        self.assert_involvements_complete(involvements.rows)
        investors = wb["Investors"]
        self.assertGreater(len([row for row in investors.rows]), 1)
        self.assert_investors_complete(investors.rows)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_without_group(self):
        response = self.client.get(reverse("export", kwargs={"format": "xls"}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_group(self):
        response = self.client.get(
            reverse("export", kwargs={"format": "xls", "group": "target_country"})
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_group_value(self):
        response = self.client.get(
            reverse(
                "export",
                kwargs={"format": "xls", "group": "intention", "group_value": "Mining"},
            )
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_group_value_country(self):
        response = self.client.get(
            reverse(
                "export",
                kwargs={
                    "format": "xls",
                    "group": "target_country",
                    "group_value": "myanmar",
                },
            )
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_group_value_region(self):
        response = self.client.get(
            reverse(
                "export",
                kwargs={
                    "format": "xls",
                    "group": "target_region",
                    "group_value": "asia",
                },
            )
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_group_value_crop(self):
        response = self.client.get(
            reverse(
                "export",
                kwargs={"format": "xls", "group": "crops", "group_value": "accacia"},
            )
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_deal_as_anonymous(self):
        response = self.client.get(
            reverse("export", kwargs={"format": "xls", "deal_id": "1"})
        )
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_deal_as_reporter(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(
            reverse("export", kwargs={"format": "xls", "deal_id": "1"})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xls_with_deal_as_reporter(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("export", kwargs={"format": "xls", "deal_id": "1"})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_csv(self):
        response = self.client.get(reverse("export", kwargs={"format": "csv"}))
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/x-zip-compressed", response["Content-Type"])
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        file_names = ["deals.csv", "involvements.csv", "investors.csv"]
        self.assertEqual(file_names, zip_file.namelist())
        for file_name in file_names:
            file_content = zip_file.open(file_name).read()
            reader = csv.reader(file_content.decode("utf-8"))
            rows = [row for row in reader]
            self.assertGreater(len(rows), 1)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_xml(self):
        response = self.client.get(reverse("export", kwargs={"format": "xml"}))
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/xml", response["Content-Type"])
        root = ET.fromstring(response.content.decode("utf-8"))
        self.assertEqual(3, len(root))
        # Deals
        deals = root.find("deals")
        self.assertIsNotNone(deals)
        self.assertGreater(len(deals.findall("item")), 0)
        # Involvements
        involvements = root.find("involvements")
        self.assertIsNotNone(involvements)
        self.assertGreater(len(involvements.findall("item")), 0)
        # Investors
        investors = root.find("investors")
        self.assertIsNotNone(investors)
        self.assertGreater(len(investors.findall("item")), 0)
