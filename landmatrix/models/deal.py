from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Activity, ActivityAttributeGroup, Country

from django.db.models import Max
import itertools


class Indexable:

    def __init__(self, it):
        self.iterable = iter(it)
        self.already_computed = []

    def __iter__(self):
        for element in self.iterable:
            self.already_computed.append(element)
            yield element

    def __getitem__(self, index):
        try:
            max_idx = index.stop
        except AttributeError:
            max_idx = index
        n = max_idx-len(self.already_computed)+1
        if n > 0:
            self.already_computed.extend(itertools.islice(self.iterable, n))
        return self.already_computed[index]


class Deal:

    class Manager:

        def all(self):
            return Indexable(Deal(deal_id['activity_identifier']) for deal_id in Activity.objects.values('activity_identifier').distinct())

    objects = Manager()

    def __init__(self, deal_id=None):
        if deal_id is not None:
            self._set_activity(get_latest_activity(deal_id))

    def __str__(self):
        return str(
                {
                    'attributes': self.attributes, 'operational stakeholder': self.operational_stakeholder,
                    'stakeholders': self.stakeholders
                }
        )

    @classmethod
    def from_activity(cls, activity):
        deal = Deal()
        deal._set_activity(activity)
        return deal

    def get_activity_attributes(self):
        attributes = ActivityAttributeGroup.objects.filter(fk_activity=self.activity).values('attributes')
        attributes_list = [a['attributes'] for a in attributes]
        return aggregate_activity_attributes(attributes_list, {})

    def get_operational_stakeholder(self):
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity=self.activity)
        if len(involvements) > 1:
            raise RuntimeError('More than one OP for activity %s: %s' % (str(self.activity), str(involvements)))
        if len(involvements) < 1:
            raise RuntimeError('No OP for activity %s: %s' % (str(self.activity), str(involvements)))
        return Investor.objects.get(pk=involvements[0].fk_investor_id)

    def get_stakeholders(self):
        stakeholder_involvements = InvestorVentureInvolvement.objects.filter(fk_venture=self.operational_stakeholder.pk)
        return [Investor.objects.get(pk=involvement.fk_investor_id) for involvement in stakeholder_involvements]

    def attribute_groups(self):
        return ActivityAttributeGroup.objects.filter(fk_activity=self.activity)

    def get_history(self):
        return [Deal.from_activity(activity)
                for activity in  self.activity.history.filter(activity_identifier=self.activity.activity_identifier)]

    def _set_activity(self, activity):
        self.id = activity.activity_identifier
        self.activity = activity
        self.attributes = self.get_activity_attributes()
        self.operational_stakeholder = self.get_operational_stakeholder()
        self.stakeholders = self.get_stakeholders()


def get_latest_activity(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).last()
    # version_max = _get_latest_version(deal_id)
    # return Activity.objects.filter(activity_identifier=deal_id, version=version_max).last()


def aggregate_activity_attributes(attributes_list, already_set_attributes):
    if not attributes_list:
        return already_set_attributes

    for key, value in attributes_list.pop(0).items():
        update_attributes(already_set_attributes, key, value)

    return aggregate_activity_attributes(attributes_list, already_set_attributes)


def update_attributes(attributes, key, value):
    if key in ['type', 'url', 'file']:
        attributes[key] = attributes.get(key, []) + [value]
    else:
        attributes[key] = resolve_country(key, value)


def resolve_country(key, value):
    return Country.objects.get(id=int(value)).name if 'country' in key and value.isdigit() else value


# def get_stakeholder_attributes(stakeholder):
#     attributes = StakeholderAttributeGroup.objects.filter(fk_stakeholder=stakeholder).values('attributes')
#     return {key: resolve_country(key, value) for a in attributes for key, value in a['attributes'].items()}


def _get_latest_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']


def _get_latest_stakeholder_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']

