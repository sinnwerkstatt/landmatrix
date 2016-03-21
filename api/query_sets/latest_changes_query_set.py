from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

from django_comments.models import Comment

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class LatestChangesQuerySet:

    DEFAULT_NUM_CHANGES = 5

    def __init__(self, request):
        self.num_changes = int(request.GET.get('n', self.DEFAULT_NUM_CHANGES))

    def all(self):
        deal_data = [
            deal_to_data(activity, activity.history_date, status_string(activity.fk_status))
            for activity in (self.get_latest_activities())
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
        return [(Activity.objects.get(pk=comment.object_pk), comment) for comment in latest_comments]

    def get_latest_activities(self):
        return Activity.history.filter(fk_status_id__in=(2, 3, 4)).order_by('-history_date')[:self.num_changes]


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
        'deal_id': activity.activity_identifier, 'change_date': change_date.strftime('%Y-%m-%d %H:%M'), 'action': action,
        'target_country': target_country(activity)
    }


def target_country(activity):
    attributes = ActivityAttributeGroup.objects.filter(fk_activity_id=activity.id).order_by('-id')
    for group in attributes:
        if 'target_country' in group.attributes:
            return group.attributes['target_country']
    raise ValueError('No target_country in attributes for activity ()'.format(activity.id))

