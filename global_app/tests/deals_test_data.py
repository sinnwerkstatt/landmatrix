__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *

from datetime import date

class DealsTestData:

    PI_NAME = 'This should be a darn unique investor name, right?'
    INTENTION = 'Livestock'
    MINIMAL_POST = { "filters": { "group_by": "all" }, "columns": ["primary_investor", "intention"] }
    LIST_POST = { "filters": { "group_by": "all" }, "columns": ["primary_investor", "intention"] }
    TYPICAL_POST = {
        "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
        "columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"]
    }
    ACT_ID = 1

    activity_version = 0
    def make_involvement(self, i_r = 0.):
        self.make_language()
        self.activity_version += 1
        act = Activity(fk_status=Status.objects.get(id=2), activity_identifier=self.ACT_ID, version=self.activity_version)
        act.save()
        pi = PrimaryInvestor(fk_status=Status.objects.get(id=2), primary_investor_identifier=1, version=1, name=self.PI_NAME)
        pi.save()
        sh = Stakeholder(fk_status=Status.objects.get(id=2), stakeholder_identifier=1, version=1)
        sh.save()
        i = Involvement(fk_activity=act, fk_stakeholder=sh, fk_primary_investor = pi, investment_ratio=i_r)
        i.save()
        return i

    def create_data(self):
        self.make_involvement(1.23)
        Region(
            name='South-East Asia', slug='south-east-asia', point_lat=0., point_lon=120.
        ).save()
        Country(
            fk_region=Region.objects.last(), code_alpha2='LA', code_alpha3='LAO',
            name="Lao People's Democratic Republic", slug='lao-peoples-democratic-republic',
            point_lat=18.85627, point_lon=106.495496,
            democracy_index=2.10, corruption_perception_index=2.1, high_income=False
        ).save()
        aag = ActivityAttributeGroup(
            fk_activity = Activity.objects.last(),
            fk_language=Language.objects.last(),
            date=date.today(),
            attributes={
                'intention': self.INTENTION, 'pi_deal': 'True', 'deal_scope': 'transnational',
                'target_country': Country.objects.last().id
            }
        )
        aag.save()

    def create_activity_with_status(self, status_id, act_id = 0, version=1):
        self.make_language()
        if not act_id: act_id = self.ACT_ID
        Activity(fk_status=Status.objects.get(id=status_id), activity_identifier=act_id, version=version).save()

    def add_attributes_to_activity(self, activity, attributes):
        ActivityAttributeGroup(fk_activity=activity, fk_language_id=1, date=date.today(),attributes=attributes).save()

    def make_language(self):
        if len(Language.objects.all()) > 0: return
        Language(english_name='English', local_name='English', locale='en').save()