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

    def __init__(self, id):
        self.id = id

        self.activity = get_latest_activity(id)
        self.attributes = self.get_activity_attributes()

        primary_investor_ids, stakeholder_ids = self.get_pi_and_sh_id()

        # last() always has latest version, no need for MAX() gymnastics
#        self.primary_investor = PrimaryInvestor.objects.filter(id__in=primary_investor_ids).last()
        self.stakeholder = get_stakeholder(stakeholder_ids)
        self.stakeholders = get_stakeholders(stakeholder_ids)

    def __str__(self):
        return str({'attributes': self.attributes, 'primary_investor': self.primary_investor, 'stakeholder': self.stakeholder})

    def get_activity_attributes(self):
        attributes = ActivityAttributeGroup.objects.filter(fk_activity=self.activity).values('attributes')
        attributes_list = [a['attributes'] for a in attributes]
        return aggregate_activity_attributes(attributes_list, {})

    def get_pi_and_sh_id(self):
        involvements = self.involvement_set().values('fk_primary_investor_id', 'fk_stakeholder_id')
        return [i['fk_primary_investor_id'] for i in involvements], [i['fk_stakeholder_id'] for i in involvements]

    def involvement_set(self):
#        return Involvement.objects.select_related().filter(fk_activity=self.activity)
        return None

    def attribute_groups(self):
        return ActivityAttributeGroup.objects.filter(fk_activity=self.activity)


def get_latest_activity(deal_id):
    version_max = _get_latest_version(deal_id)
    return Activity.objects.filter(activity_identifier=deal_id, version=version_max).last()


# def get_stakeholders(ids):
#     return Stakeholder.objects.filter(id__in=ids)


# def get_stakeholder(stakeholder_ids):
#     sh = get_stakeholders(stakeholder_ids).last()
#     return get_stakeholder_attributes(sh)


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

