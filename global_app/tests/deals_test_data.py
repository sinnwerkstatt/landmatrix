__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *

from datetime import date

class DealsTestData:

    OS_NAME = 'This should be a darn unique investor name, right?'
    INTENTION = 'Livestock'
    MINIMAL_POST = { "filters": { "group_by": "all" }, "columns": ["operational_stakeholder", "intention"] }
    LIST_POST = { "filters": { "group_by": "all" }, "columns": ["operational_stakeholder", "intention"] }
    TYPICAL_POST = {
        "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
        "columns": [
            "deal_id", "target_country", "operational_stakeholder", "stakeholder_name", "stakeholder_country",
            "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"
        ]
    }
    ACT_ID = 1

    region = None
    country = None

    activity_version = 0
    def make_involvement(self, i_r = 0.):
        self.make_language()
        self.activity_version += 1
        act = Activity(fk_status=Status.objects.get(id=2), activity_identifier=self.ACT_ID, version=self.activity_version)
        act.save()
        self.make_investor_activity_involvement(act, i_r)

    def make_investor_activity_involvement(self, activity, i_r = 0.):
        from django.utils import timezone
        investor = Investor(
            investor_identifier=1, name=self.OS_NAME, fk_status=Status.objects.get(id=2), timestamp=timezone.now(), version=1
        )
        investor.save()
        investor_activity_involvement = InvestorActivityInvolvement(
            fk_activity=activity, fk_investor=investor, percentage=i_r, fk_status=Status.objects.get(id=2), timestamp=timezone.now()
        )
        investor_activity_involvement.save()

    def create_data(self):
        self.make_involvement()
        self.create_country()
        ActivityAttributeGroup(
            fk_activity=Activity.objects.last(),
            fk_language=Language.objects.last(),
            date=date.today(),
            attributes={
                'intention': self.INTENTION,
                'target_country': Country.objects.last().id
            }
        ).save()
        PublicInterfaceCache(
            fk_activity=Activity.objects.last(),
            is_deal=True,
            deal_scope='transnational'
        ).save()

    def create_country(self):
        if self.region: return
        self.region = Region(
            name='South-East Asia', slug='south-east-asia', point_lat=0., point_lon=120.
        )
        self.region.save()
        self.country = Country(
            fk_region=Region.objects.last(), code_alpha2='KH', code_alpha3='KHM',
            name="Cambodia", slug='cambodia',
            point_lat=12.565679, point_lon=104.990963,
            democracy_index=4.87, corruption_perception_index=2.2, high_income=False
        )
        self.country.save()

    def create_activity_with_status(self, status_id, act_id = 0, version=1):
        self.make_language()
        if not act_id: act_id = self.ACT_ID
        Activity(fk_status=Status.objects.get(id=status_id), activity_identifier=act_id, version=version).save()

    def add_attributes_to_activity(self, activity, attributes):
        ActivityAttributeGroup(fk_activity=activity, fk_language_id=1, date=date.today(),attributes=attributes).save()

    def make_language(self):
        if len(Language.objects.all()) > 0: return
        Language(english_name='English', local_name='English', locale='en').save()