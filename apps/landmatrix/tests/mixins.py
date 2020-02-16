from copy import copy

from apps.grid.forms.deal_contract_form import DealContractForm
from apps.grid.forms.deal_data_source_form import DealDataSourceForm
from apps.grid.forms.deal_spatial_form import DealSpatialForm
from apps.grid.views.utils import DEAL_FORMS
from apps.landmatrix.models import HistoricalActivity, HistoricalInvestor, \
    HistoricalInvestorActivityInvolvement, HistoricalInvestorVentureInvolvement, \
    ActivityAttributeGroup


class ActivitiesFixtureMixin:

    activities = []
    act_fixtures = []
    act_fixtures_default = {
        "fk_status_id": "2"
    }
    attr_fixtures = []
    attr_fixtures_default = {
        "target_country": {"value": "104"},
    }
    attr_fixtures_default_type = {
        "ModelChoiceField": lambda f, v: {
            "value": f.queryset.model.objects.first().id
        },
        "ChoiceField": lambda f, v: {"value": f.choices[0][0]},
        "MultiValueField": lambda f, v: [
            {
                "value": v,
                "value2": v,
                "date": "2000",
                "is_current": True,
            },
        ],
        "default": lambda f, v: {"value": v},
    }
    attr_groups = [
        {"pk": 1, "name": "overall"},
        {"pk": 10, "name": "location_01"},
        {"pk": 20, "name": "data_source_01"},
        {"pk": 30, "name": "contract_01"},
    ]

    fixtures = [
        "languages",
        "countries_and_regions",
        "users_and_groups",
        "status",
        "investors",
        "venture_involvements",
    ]

    @classmethod
    def _get_activity_attribute_group(cls, name):
        for form in [DealSpatialForm, DealDataSourceForm, DealContractForm]:
            if name in form.base_fields.keys():
                return list(filter(lambda g: form.Meta.name in g['name'],
                                   cls.attr_groups))[0]["pk"]
        return cls.attr_groups[0]["pk"]

    @classmethod
    def _create_activity_fixtures(cls):
        # Create activity attribute groups
        for group in cls.attr_groups:
            ActivityAttributeGroup.objects.get_or_create(**group)

        # Create activity and activity attributes
        act_fixtures, attr_fixtures = [], []
        for act_attributes in cls.act_fixtures:
            act_fixture = copy(cls.act_fixtures_default)
            act_fixture.update({k: v for k, v in act_attributes.items()
                                if k != "attributes"})
            attr_fixture = act_attributes.get("attributes")
            for form in DEAL_FORMS:
                form = hasattr(form, "form") and form.form or form
                for i, (name, field) in enumerate(form.base_fields.items()):
                    if name.startswith("tg_") and not name.endswith("_comment"):
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
                    if not 'fk_group_id' in attr:
                        attr['fk_group_id'] = cls._get_activity_attribute_group(name)
                    attr_fixture[name] = attr
            act_fixtures.append(act_fixture)
            attr_fixtures.append(attr_fixture)
        return act_fixtures, attr_fixtures

    @classmethod
    def load_activity_fixtures(cls):
        act_fixtures, attr_fixtures = cls._create_activity_fixtures()

        activities = []
        for i, act_fixture in enumerate(act_fixtures):
            activity = HistoricalActivity.objects.create(**act_fixture)
            for name, attribute in attr_fixtures[i].items():
                if not isinstance(attribute, (list, tuple)):
                    attribute = [attribute]
                for attr in attribute:
                    activity.attributes.create(name=name, **attr)
            activities.append(activity)
        cls.activities = activities

    def setUp(self):
        super().setUp()
        self.load_activity_fixtures()


class InvestorsFixtureMixin:

    investors = []
    inv_fixtures = []
    inv_fixtures_default = lambda a: {
        "name": "name",
        "fk_country_id": "104",
        "classification": "10",
        "homepage": "https://www.example.com",
        "opencorporates_link": "https://opencorporates.com/companies/de/1",
        "comment": "comment",
        "fk_status_id": "2",
    }

    @classmethod
    def load_investor_fixtures(cls):
        investors = []
        for inv_attributes in cls.inv_fixtures:
            attributes = cls.inv_fixtures_default(inv_attributes)
            attributes.update(inv_attributes)
            investor = HistoricalInvestor.objects.create(**attributes)
            investors.append(investor)
        cls.investors = investors

    def setUp(self):
        super().setUp()
        self.load_investor_fixtures()


class InvestorActivityInvolvementsFixtureMixin:

    act_involvements = []
    act_inv_fixtures = {
    }

    @classmethod
    def load_activity_involvement_fixtures(cls):
        involvements = []
        for activity, investor in cls.act_inv_fixtures.items():
            involvement = HistoricalInvestorActivityInvolvement.objects.create(
                fk_activity_id=activity,
                fk_investor_id=investor,
                fk_status_id=2
            )
            involvements.append(involvement)
        cls.act_involvements = involvements

    def setUp(self):
        super().setUp()
        self.load_activity_involvement_fixtures()


class InvestorVentureInvolvementsFixtureMixin:

    inv_involvements = []
    inv_inv_fixtures = []
    inv_inv_fixtures_default = lambda i: {
        "role": "ST",
        "investment_type": 10,
        "percentage": 100.0,
        "loans_amount": 10.0,
        "loans_currency_id": 49,
        "parent_relation": "Subsidiary",
        "comment": "comment",
        "fk_status_id": "2",
    }

    @classmethod
    def load_investor_involvement_fixtures(cls):
        involvements = []
        for inv_attributes in cls.inv_inv_fixtures:
            attributes = cls.inv_inv_fixtures_default(inv_attributes)
            attributes.update(inv_attributes)
            involvement = HistoricalInvestorVentureInvolvement.objects.create(**inv_attributes)
            involvements.append(involvement)
        cls.inv_involvements = involvements

    def setUp(self):
        super().setUp()
        self.load_investor_involvement_fixtures()
