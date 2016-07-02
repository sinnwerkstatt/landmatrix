from django_comments.models import Comment

from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.country import Country


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class LatestChangesQuerySet:

    DEFAULT_NUM_CHANGES = 5

    def __init__(self, request):
        self.num_changes = int(request.GET.get('n', self.DEFAULT_NUM_CHANGES))
        self.country = request.GET.get('target_country')
        self.region = request.GET.get('target_region')

    def all(self):
        deal_data = [
            deal_to_data(activity, activity.history_date, status_string(activity.fk_status))
            for activity in self.get_latest_activities()
        ]
        deal_data += [
            deal_to_data(activity, comment.submit_date, 'comment')
            for activity, comment in (self.get_latest_commented())
        ]

        deal_data = remove_duplicates(deal_data)
        deal_data = sorted(deal_data, key=lambda d: d['change_date'], reverse=True)
        return deal_data[:self.num_changes]

    def get_latest_commented(self):
        latest_comments = Comment.objects.filter(is_public=True).order_by('-submit_date')[:self.num_changes]
        return [
            (Activity.objects.get(pk=comment.object_pk), comment)
            for comment in latest_comments
            if self.is_in_desired_region(comment)
        ]

    def is_in_desired_region(self, comment):
        base_query = Activity.objects.filter(pk=comment.object_pk)
        if self.country:
            base_query = base_query.filter(pk__in=self.activity_ids_by_country())
        if self.region:
            base_query = base_query.filter(pk__in=self.activity_ids_by_region())
        return base_query.exists()

    def get_latest_activities(self):
        all_activities = HistoricalActivity.objects.filter(fk_status_id__in=(2, 3, 4))
        if self.country:
            all_activities = all_activities.filter(id__in=self.activity_ids_by_country())
        if self.region:
            all_activities = all_activities.filter(id__in=self.activity_ids_by_region())
        return all_activities.order_by('-history_date')[:self.num_changes]

    def activity_ids_by_country(self):
        return ActivityAttribute.objects.filter(
            name='target_country', value=self.country
        ).values_list('fk_activity_id', flat=True).distinct()

    def activity_ids_by_region(self):
        countries_in_region = Country.objects.filter(fk_region_id=self.region).values_list('id', flat=True).distinct()
        return ActivityAttribute.objects.filter(
            name='target_country', value__in=list(countries_in_region)
        ).values_list('fk_activity_id', flat=True).distinct()

def remove_duplicates(deal_data):
    deal_ids = []
    deals = []
    for deal in deal_data:
        if not deal['deal_id'] in deal_ids:
            deal_ids.append(deal['deal_id'])
            deals.append(deal)
    return deals


def status_string(status):
    return 'add' if status.id == 2 else 'change' if status.id == 3 else 'delete' if status.id == 4 else 'wrong'


def deal_to_data(activity, change_date, action):
    return {
        'deal_id': activity.activity_identifier, 'change_date': change_date, 'action': action,
        'target_country': target_country(activity)
    }


def target_country(activity):
    country = ActivityAttribute.objects.filter(fk_activity_id=activity.id, name='target_country').order_by('-id')
    if country.count() > 0:
        return Country.objects.get(pk=country[0].value).name
    else:
        raise ValueError('No target_country in attributes for activity ()'.format(activity.id))

