from collections import OrderedDict
from copy import copy

from datetime import datetime

import pytz
from django.core.management import call_command
from django import forms
from django.test import override_settings

from apps.api.elasticsearch import es_save
from apps.grid.fields import YearBasedChoiceField, YearBasedMultipleChoiceIntegerField
from apps.grid.forms.deal_contract_form import DealContractForm
from apps.grid.forms.deal_data_source_form import DealDataSourceForm
from apps.grid.forms.deal_spatial_form import DealSpatialForm
from apps.grid.views.utils import DEAL_FORMS
from apps.landmatrix.models import (
    HistoricalActivity,
    HistoricalInvestor,
    HistoricalInvestorActivityInvolvement,
    HistoricalInvestorVentureInvolvement,
    ActivityAttributeGroup,
    InvestorActivityInvolvement,
    Investor,
    Activity,
    InvestorVentureInvolvement,
    Country,
)


class ActivitiesFixtureMixin:

    act_fixtures = []
    act_fixtures_default = {
        "fk_status_id": 2,
        "history_date": datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc),
        "history_user_id": 1,
    }
    attr_fixtures = []
    attr_fixtures_default = {
        "target_country": {"value": "104"},
        "negotiation_status": {"value": "Contract signed", "date": "2000"},
        "contract_area": {"value": None},
        "intended_area": {"value": None},
        "production_area": {"value": None},
        "not_public": {"value": "False"},
        "contract_size": {"value": "200"},
    }
    attr_fixtures_default_type = {
        forms.ModelChoiceField: lambda f, v: {
            "value": f.queryset.model.objects.first()
            and f.queryset.model.objects.first().id
        },
        forms.ChoiceField: lambda f, v: {"value": f.choices[0][0] or f.choices[1][0]},
        YearBasedChoiceField: lambda f, v: {
            "value": f.choices[0][0] or f.choices[1][0]
        },
        YearBasedMultipleChoiceIntegerField: lambda f, v: {
            "value": f.choices[0][0] or f.choices[1][0]
        },
        forms.MultiValueField: lambda f, v: [
            {"value": v, "value2": v, "date": "2000", "is_current": True}
        ],
        forms.BooleanField: lambda f, v: {"value": "True"},
        forms.Field: lambda f, v: {"value": v},
    }
    attr_groups = [
        {"pk": 1, "name": "overall"},
        {"pk": 2, "name": "location_01"},
        {"pk": 3, "name": "data_source_01"},
        {"pk": 4, "name": "contract_01"},
        {"pk": 5, "name": "investor_info"},
    ]

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
        "crops",
        "animals",
        "minerals",
        "currencies",
    ]

    _act_fixtures = []
    _attr_fixtures = []
    _activity_ids = []
    _historical_attributes = [
        "history_user",
        "history_user_id",
        "history_date",
        "fully_updated",
    ]

    @classmethod
    def _get_activity_attribute_group(cls, name):
        for form in [DealSpatialForm, DealDataSourceForm, DealContractForm]:
            if name in form.base_fields.keys():
                return list(
                    filter(lambda g: form.Meta.name in g["name"], cls.attr_groups)
                )[0]["pk"]
        return cls.attr_groups[0]["pk"]

    @classmethod
    def _create_activity_fixtures(cls):
        if cls._act_fixtures:
            return

        act_fixtures, attr_fixtures = [], []
        for act_attributes in cls.act_fixtures:
            act_fixture = copy(cls.act_fixtures_default)
            act_fixture.update(
                {k: v for k, v in act_attributes.items() if k != "attributes"}
            )
            attr_fixture = act_attributes.get("attributes", {})
            for form in DEAL_FORMS:
                form = hasattr(form, "form") and form.form or form
                for i, (name, field) in enumerate(form.base_fields.items()):
                    if name.startswith("tg_") and not name.endswith("_comment"):
                        continue
                    if name in attr_fixture:
                        attr = attr_fixture.get(name)
                    elif f"{name}_id" in attr_fixture:
                        name = f"{name}_id"
                        attr = attr_fixture.get(name)
                    elif name in cls.attr_fixtures_default:
                        attr = cls.attr_fixtures_default.get(name)
                    elif f"{name}_id" in cls.attr_fixtures_default:
                        name = f"{name}_id"
                        attr = cls.attr_fixtures_default.get(name)
                    else:
                        field_class = type(field)
                        for key, value in cls.attr_fixtures_default_type.items():
                            if issubclass(field_class, key):
                                attr = value
                                break
                        if not attr:
                            attr = cls.attr_fixtures_default_type.get("default")
                    if callable(attr):
                        attr = attr(field, str(i))
                    if not isinstance(attr, (list, tuple)):
                        attr = [attr]
                    for attr_dict in attr:
                        if attr_dict and not "fk_group_id" in attr_dict:
                            attr_dict[
                                "fk_group_id"
                            ] = cls._get_activity_attribute_group(name)
                    attr_fixture[name] = attr
            act_fixtures.append(act_fixture)
            attr_fixtures.append(attr_fixture)
        cls._act_fixtures = act_fixtures
        cls._attr_fixtures = attr_fixtures

    @classmethod
    def load_activity_fixtures(cls):
        cls._create_activity_fixtures()

        # Create activity attribute groups
        for group in cls.attr_groups:
            ActivityAttributeGroup.objects.get_or_create(**group)

        # Create activity and activity attributes
        dact_fixtures = OrderedDict()
        for i, act_fixture in enumerate(cls._act_fixtures):
            activity = HistoricalActivity.objects.create(**act_fixture)
            for name, attribute in cls._attr_fixtures[i].items():
                if not isinstance(attribute, (list, tuple)):
                    attribute = [attribute]
                for attr in attribute:
                    if attr:
                        activity.attributes.create(name=name, **attr)

            dact_fixture = copy(act_fixture)
            for attr in cls._historical_attributes:
                dact_fixture.pop(attr, None)
            dact_fixtures[str(activity.activity_identifier)] = dact_fixture
        # Deprecated soon...
        cls._activity_ids = [str(a.get("id")) for a in dact_fixtures.values()]
        for id, fixture in dact_fixtures.items():
            activity = Activity.objects.create(**fixture)
            for name, attribute in cls._attr_fixtures[i].items():
                if not isinstance(attribute, (list, tuple)):
                    attribute = [attribute]
                for attr in attribute:
                    if attr:
                        activity.attributes.create(name=name, **attr)

    @classmethod
    def unload_activity_fixtures(cls):
        ActivityAttributeGroup.objects.all().delete()
        HistoricalActivity.objects.all().delete()
        Activity.objects.all().delete()

    def setUp(self):
        self.load_activity_fixtures()
        super().setUp()

    def tearDown(self):
        self.unload_activity_fixtures()
        super().tearDown()


class InvestorsFixtureMixin:

    inv_fixtures = []
    inv_fixtures_default = lambda a: {
        "name": "name",
        "fk_country": Country.objects.get(id=116),
        "classification": "10",
        "homepage": "https://www.example.com",
        "opencorporates_link": "https://opencorporates.com/companies/de/1",
        "comment": "comment",
        "fk_status_id": 2,
        "history_date": datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc),
        "history_user_id": 1,
    }

    _inv_fixtures = []
    _investor_ids = []
    _historical_attributes = [
        "history_user",
        "history_user_id",
        "history_date",
        "fully_updated",
    ]

    @classmethod
    def _create_investor_fixtures(cls):
        if cls._inv_fixtures:
            return
        fixtures = []
        for inv_attributes in cls.inv_fixtures:
            attributes = cls.inv_fixtures_default(inv_attributes)
            attributes.update(inv_attributes)
            fixtures.append(attributes)
        cls._inv_fixtures = fixtures

    @classmethod
    def load_investor_fixtures(cls):
        cls._create_investor_fixtures()
        inv_fixtures = OrderedDict()
        for fixture in cls._inv_fixtures:
            investor = HistoricalInvestor.objects.create(**fixture)

            inv_fixture = copy(fixture)
            for attr in cls._historical_attributes:
                inv_fixture.pop(attr, None)
            inv_fixtures[str(investor.investor_identifier)] = inv_fixture
        # Deprecated soon..
        cls._investor_ids = [str(i.get("id")) for i in inv_fixtures.values()]
        for id, fixture in inv_fixtures.items():
            Investor.objects.create(**fixture)

    @classmethod
    def unload_investor_fixtures(cls):
        HistoricalInvestor.objects.all().delete()
        Investor.objects.all().delete()

    def setUp(self):
        self.load_investor_fixtures()
        super().setUp()

    def tearDown(self):
        self.unload_investor_fixtures()
        super().tearDown()


class InvestorActivityInvolvementsFixtureMixin:

    act_inv_fixtures = {}

    _act_inv_fixtures = []

    @classmethod
    def _create_activity_involvement_fixtures(cls):
        if cls._act_inv_fixtures:
            return
        fixtures = []
        for activity, investor in cls.act_inv_fixtures.items():
            fixtures.append(
                {
                    "fk_activity_id": activity,
                    "fk_investor_id": investor,
                    "fk_status_id": 2,
                }
            )
        cls._act_inv_fixtures = fixtures

    @classmethod
    def load_activity_involvement_fixtures(cls):
        cls._create_activity_involvement_fixtures()
        for fixture in cls._act_inv_fixtures:
            HistoricalInvestorActivityInvolvement.objects.create(**fixture)
            # Deprecated soon...
            if (
                str(fixture.get("fk_activity_id")) in cls._activity_ids
                and str(fixture.get("fk_investor_id")) in cls._investor_ids
            ):
                involvement = InvestorActivityInvolvement.objects.create(**fixture)
                involvement.fk_activity.refresh_cached_attributes()

    @classmethod
    def unload_activity_involvement_fixtures(cls):
        HistoricalInvestorActivityInvolvement.objects.all().delete()
        InvestorActivityInvolvement.objects.all().delete()

    def setUp(self):
        self.load_activity_involvement_fixtures()
        super().setUp()

    def tearDown(self):
        self.unload_activity_involvement_fixtures()
        super().tearDown()


class InvestorVentureInvolvementsFixtureMixin:

    fixtures = ["status", "countries_and_regions", "users_and_groups", "currencies"]

    inv_involvements = []
    inv_inv_fixtures = []
    inv_inv_fixtures_default = lambda i: {
        "role": "ST",
        "investment_type": ["10"],
        "percentage": 100.0,
        "loans_amount": 10.0,
        "loans_currency_id": 49,
        "parent_relation": "Subsidiary",
        "comment": "comment",
        "fk_status_id": 2,
    }

    _inv_inv_fixtures = []

    @classmethod
    def _create_investor_involvement_fixtures(cls):
        if cls._inv_inv_fixtures:
            pass
        fixtures = []
        for inv_attributes in cls.inv_inv_fixtures:
            fixture = cls.inv_inv_fixtures_default(inv_attributes)
            fixture.update(inv_attributes)
            fixtures.append(fixture)
        cls._inv_inv_fixtures = fixtures

    @classmethod
    def load_investor_involvement_fixtures(cls):
        cls._create_investor_involvement_fixtures()
        for fixture in cls._inv_inv_fixtures:
            HistoricalInvestorVentureInvolvement.objects.create(**fixture)
            # Deprecated soon...
            if (
                str(fixture.get("fk_venture_id")) in cls._investor_ids
                and str(fixture.get("fk_investor_id")) in cls._investor_ids
            ):
                InvestorVentureInvolvement.objects.create(**fixture)

    @classmethod
    def unload_investor_involvement_fixtures(cls):
        HistoricalInvestorVentureInvolvement.objects.all().delete()
        InvestorVentureInvolvement.objects.all().delete()

    def setUp(self):
        self.load_investor_involvement_fixtures()
        super().setUp()

    def tearDown(self):
        self.unload_investor_involvement_fixtures()
        super().tearDown()


class ElasticSearchFixtureMixin(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
):

    fixtures = []

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
            "filters",
        ]
        for fixture in fixtures:
            call_command("loaddata", fixture, **{"verbosity": 0})

        cls.create_fixture()

        cls.load_investor_fixtures()
        cls.load_activity_fixtures()
        cls.load_activity_involvement_fixtures()
        cls.load_investor_involvement_fixtures()

        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @classmethod
    def tearDownClass(cls):
        cls.delete_fixture()
        super().tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def create_fixture(cls):
        pass

    @classmethod
    def delete_fixture(cls):
        cls.unload_investor_involvement_fixtures()
        cls.unload_activity_involvement_fixtures()
        cls.unload_investor_fixtures()
        cls.unload_activity_fixtures()
