from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from random import randint

from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.country import Country

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
    """Deprecated: Will be deleted soon"""
    
    class Manager:

        def all(self):
            activities = Activity.objects.distinct().values('activity_identifier')
            return Indexable(Deal(deal_id['activity_identifier']) for deal_id in activities)

        def filter(self, **kwargs):
            activities = Activity.objects.filter(**kwargs).distinct().values('activity_identifier')
            return Indexable(Deal(deal_id['activity_identifier']) for deal_id in activities)

    objects = Manager()

    def __init__(self, deal_id=None):
        if deal_id is not None:
            self._set_activity(get_latest_activity(deal_id))

    def __str__(self):
        return 'Deal ' + str(self.activity.activity_identifier) + ': ' + str(
                {
                    'activity': self.activity, 'attributes': self.attributes,
                    'operational stakeholder': self.operational_stakeholder, 'stakeholders': self.stakeholders
                }
        )

    def __eq__(self, other):
        if self.operational_stakeholder != other.operational_stakeholder:
            print('operational_stakeholder', self.operational_stakeholder, other.operational_stakeholder)
            return False
        if self.stakeholders != other.stakeholders:
            print('stakeholders', self.stakeholders, other.stakeholders)
            return False
        for attribute in (k for k in self.activity.__dict__.keys() if not k[0] == '_'):
            if self.activity.__dict__[attribute] != other.activity.__dict__[attribute]:
                print('activity attribute', attribute, self.activity.__dict__[attribute], other.activity.__dict__[attribute])
                return False
        for attribute in self.attributes.keys():
            random_default_value = randint()
            if getattr(self, attribute, random_default_value) != getattr(other, attribute, random_default_value):
                print('attribute', attribute, getattr(self, attribute, random_default_value) != getattr(other, attribute, random_default_value))
                return False

        return True

    @classmethod
    def from_activity(cls, activity):
        deal = cls()
        deal._set_activity(activity)
        return deal

    def get_activity_attributes(self):
        return dict(ActivityAttribute.objects.filter(fk_activity_id=self.activity.id).values_list('name', 'value'))
        #attributes = self.attribute_groups().values('attributes')
        #attributes_list = [a['attributes'] for a in attributes]
        #return aggregate_activity_attributes(attributes_list, {})

    def get_operational_stakeholder(self):
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity_id=self.activity.id)
        if len(involvements) > 1:
            raise MultipleObjectsReturned('More than one OP for activity %s: %s' % (str(self.activity), str(involvements)))
        if len(involvements) < 1:
            raise ObjectDoesNotExist('No OP for activity %s: %s' % (str(self.activity), str(involvements)))
        return Investor.objects.get(pk=involvements[0].fk_investor_id)

    def get_stakeholders(self):
        stakeholder_involvements = InvestorVentureInvolvement.objects.filter(fk_venture=self.operational_stakeholder.pk)
        return [Investor.objects.get(pk=involvement.fk_investor_id) for involvement in stakeholder_involvements]

    def _set_activity(self, activity):
        if activity is None:
            raise ObjectDoesNotExist()

        self.id = activity.activity_identifier
        self.activity = activity
        self.attributes = self.get_activity_attributes()
        self.operational_stakeholder = self.get_operational_stakeholder()
        self.stakeholders = self.get_stakeholders()


def get_latest_activity(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).last()
    # version_max = _get_latest_version(deal_id)
    # return Activity.objects.filter(activity_identifier=deal_id, version=version_max).last()


#def aggregate_activity_attributes(attributes_list, already_set_attributes):
#    if not attributes_list:
#        return already_set_attributes
#
#    for key, value in attributes_list.pop(0).items():
#        update_attributes(already_set_attributes, key, value)
#
#    return aggregate_activity_attributes(attributes_list, already_set_attributes)
#
#
#def update_attributes(attributes, key, value):
#    if key in ['type', 'url', 'file']:
#        attributes[key] = attributes.get(key, []) + [value]
#    else:
#        attributes[key] = resolve_country(key, value)


def resolve_country(key, value):
    return Country.objects.get(id=int(value)).name if 'country' in key and value.isdigit() else value


# def get_stakeholder_attributes(stakeholder):
#     attributes = StakeholderAttributeGroup.objects.filter(fk_stakeholder=stakeholder).values('attributes')
#     return {key: resolve_country(key, value) for a in attributes for key, value in a['attributes'].items()}


def _get_latest_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']


def _get_latest_stakeholder_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']

