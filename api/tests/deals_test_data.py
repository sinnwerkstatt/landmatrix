__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *

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
        from datetime import date
        self.make_involvement(1.23)
        self._generate_language()
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
            fk_language=self.language,
            date=date.today(),
            attributes={
                'intention': self.INTENTION, 'pi_deal': 'True', 'deal_scope': 'transnational',
                'target_country': Country.objects.last().id
            }
        )
        aag.save()

    language = None
    def _generate_language(self):
        self.language = Language(english_name='English', local_name='Dinglisch', locale='en')
        self.language.save()

    def create_activity_with_status(self, status_id, act_id = 0, version=1):
        if not act_id: act_id = self.ACT_ID
        Activity(fk_status=Status.objects.get(id=status_id), activity_identifier=act_id, version=version).save()

    DEFAULT_TRANSNATIONAL_DEAL_ID = 123
    DEFAULT_DOMESTIC_DEAL_ID = 124

    def _generate_transnational_negotiation_status_data(self, preset_id=DEFAULT_TRANSNATIONAL_DEAL_ID):
        self._generate_negotiation_status_data(preset_id, {'pi_deal_size': '12345', 'deal_scope': 'transnational'})

    def _generate_domestic_negotiation_status_data(self, preset_id=DEFAULT_DOMESTIC_DEAL_ID):
        self._generate_negotiation_status_data(preset_id, {'pi_deal_size': '2345', 'deal_scope': 'domestic'})

    def _generate_negotiation_status_data(self, preset_id, deviating_attributes):
        self._generate_language()
        activity, stakeholder = self._generate_involvement(preset_id)
        self._generate_deal_country()
        attributes = {
                'intention': 'boring test stuff', 'target_country': str(self.deal_country.id),
                'pi_negotiation_status': 'Concluded (Contract signed)',
                'pi_implementation_status': 'blah', 'pi_deal': 'True', 'pi_deal_size': '2345',
                'deal_scope': 'domestic'
            }
        attributes.update(deviating_attributes)
        ac_attributes = ActivityAttributeGroup(
            fk_activity=activity, fk_language_id=1, attributes=attributes
        )
        ac_attributes.save()
        sh_attributes = StakeholderAttributeGroup(
            fk_stakeholder=stakeholder, fk_language_id=1, attributes={'country': str(self.deal_country.id)}
        )
        sh_attributes.save()

    def _generate_involvement(self, preset_id):
        activity = Activity(activity_identifier=preset_id, fk_status_id=2, version=1)
        activity.save()
        p_i = PrimaryInvestor(id=preset_id, primary_investor_identifier=preset_id, fk_status_id=2, version=1)
        p_i.save()
        stakeholder = Stakeholder(id=preset_id, stakeholder_identifier=preset_id, fk_status_id=2, version=1)
        stakeholder.save()
        involvement = Involvement(fk_activity=activity, fk_primary_investor=p_i, fk_stakeholder=stakeholder)
        involvement.save()
        return activity, stakeholder

    deal_country = None
    deal_region = None

    def _generate_deal_country(self):
        if not self.deal_country:
            self.deal_region = Region(id=123)
            self.deal_region.save()
            self.deal_country = Country(id=123, fk_region=self.deal_region)
            self.deal_country.save()

