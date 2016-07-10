from datetime import datetime

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *

class DealsTestData:

    PI_NAME = 'This should be a darn unique investor name, right?'
    STAKEHOLDER_NAME = "I'm sure this is a unique stakeholder name, yeah!"
    INTENTION = 'Livestock'
    MINIMAL_POST = { "filters": { "group_by": "all" }, "columns": ["operational_stakeholder", "intention"] }
    LIST_POST = { "filters": { "group_by": "all" }, "columns": ["operational_stakeholder", "intention"] }
    TYPICAL_POST = {
        "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
        "columns": [
            "deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention",
            "negotiation_status", "implementation_status", "intended_size", "contract_size"
        ]
    }
    ACT_ID = 1

    activity_version = 0
    def make_activity_with_new_version(self, ):
        self.activity_version += 1
        act = Activity(fk_status=Status.objects.get(id=2), activity_identifier=self.ACT_ID, version=self.activity_version)
        act.save()

    def create_data(self):
        from datetime import date
        self.make_activity_with_new_version()
        self._generate_language()
        Region(
            name='South-East Asia', slug='south-east-asia', point_lat_min=0., point_lon_min=120.
        ).save()
        Country(
            fk_region=Region.objects.last(), code_alpha2='LA', code_alpha3='LAO',
            name="Lao People's Democratic Republic", slug='lao-peoples-democratic-republic',
            point_lat_min=18.85627, point_lon_min=106.495496,
            democracy_index=2.10, corruption_perception_index=2.1, high_income=False
        ).save()
        aag = ActivityAttribute(
            fk_activity=Activity.objects.last(),
            fk_language=self.language,
            date=date.today(),
            name='intention',
            value=self.INTENTION
        )
        aag.save()
        aag = ActivityAttribute(
            fk_activity=Activity.objects.last(),
            fk_language=self.language,
            date=date.today(),
            name='target_country',
            value=Country.objects.last().id
        )
        aag.save()
        #pi = PublicInterfaceCache(
        #    fk_activity = Activity.objects.last(),
        #    is_public=True,
        #    deal_scope='transnational',
        #    timestamp=datetime.now()
        #)
        #pi.save()

    language = None
    def _generate_language(self):
        self.language = Language(english_name='English', local_name='Dinglisch', locale='en')
        self.language.save()

    def create_activity_with_status(self, status_id, act_id = 0, version=1):
        if not act_id: act_id = self.ACT_ID
        Activity(
                fk_status=Status.objects.get(id=status_id), activity_identifier=act_id,
                # version=version
        ).save()

    DEFAULT_TRANSNATIONAL_DEAL_ID = 123
    DEFAULT_DOMESTIC_DEAL_ID = 124

    def _generate_transnational_negotiation_status_data(self, preset_id=DEFAULT_TRANSNATIONAL_DEAL_ID):
        self._generate_negotiation_status_data(preset_id, 12345, 'transnational')

    def _generate_domestic_negotiation_status_data(self, preset_id=DEFAULT_DOMESTIC_DEAL_ID):
        self._generate_negotiation_status_data(preset_id, 2345, 'domestic')

    def _generate_negotiation_status_data(self, preset_id, deal_size, deal_scope, deviating_attributes=None):
        if not deviating_attributes:
            deviating_attributes = {}

        self._generate_language()
        activity = self._generate_activity(preset_id)
        self._generate_deal_country()
        self._generate_investor_country()
        attributes = {
            'intention': 'boring test stuff', 'target_country': str(self.deal_country.id),
            'investor_country': str(self.investor_country.id),
            'pi_negotiation_status': 'Concluded (Contract signed)',
            'pi_implementation_status': 'blah', 'pi_deal': 'True', 'pi_deal_size': '2345',
            'deal_scope': 'domestic'
        }
        attributes.update(deviating_attributes)
        for key, value in attributes.items():
            ac_attributes = ActivityAttribute.objects.create(
                fk_activity=activity,
                fk_language_id=1,
                name=key,
                value=value
            )

        op = self._generate_operational_stakeholder(activity, self.investor_country)
        self._generate_stakeholder(op)

        #PublicInterfaceCache(
        #    fk_activity=activity,
        #    is_public=attributes['pi_deal'],
        #    deal_scope=deal_scope,
        #    negotiation_status=attributes.get('pi_negotiation_status'),
        #    implementation_status=attributes.get('pi_implementation_status'),
        #    deal_size=deal_size
        #).save()

    def _generate_operational_stakeholder(self, activity, country=None):

        if not country:
            country = self.investor_country

        new_investor_identifier = get_latest_investor_identifier() + 1
        operational_stakeholder = Investor(
            name=self.PI_NAME, fk_country_id=country.id,
            fk_status=Status.objects.get(id=2), investor_identifier=new_investor_identifier,
            # version=1
        )
        operational_stakeholder.save()

        InvestorActivityInvolvement(
            fk_activity=activity, fk_investor=operational_stakeholder, percentage=100,
            fk_status=Status.objects.get(id=2)
        ).save()

        return operational_stakeholder

    def _generate_stakeholder(self, operational_stakeholder):
        new_investor_identifier = get_latest_investor_identifier() + 1
        stakeholder = Investor(
            name=self.STAKEHOLDER_NAME, fk_country=operational_stakeholder.fk_country, fk_status=Status.objects.get(id=2),
            investor_identifier=new_investor_identifier,
                # version=1
        )
        stakeholder.save()
        InvestorVentureInvolvement(
            fk_venture=operational_stakeholder, fk_investor=stakeholder, percentage=100,
            fk_status=Status.objects.get(id=2),
        ).save()
        return stakeholder

    def _generate_activity(self, preset_id):
        activity = Activity(
                activity_identifier=preset_id, fk_status_id=2,
                # version=1
        )
        activity.save()
        return activity

    deal_country = None
    deal_region = None

    def _generate_deal_country(self):
        if not self.deal_country:
            self.deal_region = Region(id=123)
            self.deal_region.save()
            self.deal_country = Country(id=123, name='Targetstan', fk_region=self.deal_region)
            self.deal_country.save()

    investor_country = None
    investor_region = None

    def _generate_investor_country(self):
        if not self.investor_country:
            self.investor_region = Region(id=124)
            self.investor_region.save()
            self.investor_country = Country(id=124, name='Investoria', fk_region=self.investor_region)
            self.investor_country.save()

    def _generate_countries(self, num_countries):
        self._generate_deal_country()
        self._generate_investor_country()
        for i in range(0, num_countries):
            Country(
                id=self.investor_country.id+1+i, name='Democratic Republic Of ' + str(i), fk_region=self.investor_region
            ).save()

    activity_identifiers = []
    def _generate_deal(self, investor_country, target_country, attributes):
        act_id = 1 if not self.activity_identifiers else self.activity_identifiers[-1]+1
        self.activity_identifiers.append(act_id)

        activity = self._generate_activity(act_id)
        attributes.update({
            'target_country': str(target_country.id), 'pi_deal': 'True'
        })
        for key, value in attributes.items():
            ActivityAttribute.objects.create(
                fk_activity=activity,
                fk_language_id=1,
                name=key,
                value=value
            )

        op = self._generate_operational_stakeholder(activity, investor_country)
        self._generate_stakeholder(op)
        #PublicInterfaceCache(
        #    fk_activity=activity,
        #    is_public=attributes['pi_deal'],
        #    deal_scope=attributes.get('deal_scope'),
        #    negotiation_status=attributes.get('pi_negotiation_status'),
        #    implementation_status=attributes.get('pi_implementation_status'),
        #    deal_size=attributes.get('pi_deal_size')
        #).save()


def get_latest_investor_identifier():
    from django.db.models import Max
    max_identifier = Investor.objects.values().aggregate(Max('investor_identifier'))['investor_identifier__max']
    return max_identifier if max_identifier else 0
