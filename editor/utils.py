'''
Template rendering utils.

TODO: this can all be done in the template, move it there.
'''
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from grid.templatetags.custom_tags import get_user_role

def activity_to_template(activity):
    try:
        user = activity.history_user.username
        role = get_user_role(activity.history_user)
        if role:
            user += ' (%s)' % role
    except AttributeError:
        # User doesn't exist anymore
        user = _('Deleted User')

    history_date = timezone.localtime(
        activity.history_date, timezone.get_current_timezone())

    template_data = {
        'id': activity.pk,
        'deal_id': activity.activity_identifier,
        'history_id': activity.id,
        'user': user,
        'timestamp': history_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': activity.fk_status,
        'comment': activity.comment,
    }

    return template_data


def feedback_to_template(feedback):
    timestamp = timezone.localtime(
        feedback.timestamp, timezone.get_current_timezone())
    template_data = {
        'deal_id': feedback.fk_activity.activity_identifier,
        'history_id': feedback.fk_activity_id,
        'from_user': feedback.fk_user_created.username,
        'comment': feedback.comment,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    }

    return template_data


def reject_to_template(activity):
    history_date = timezone.localtime(
        activity.history_date, timezone.get_current_timezone())
    user = activity.changesets.first().fk_user.username

    template_data = {
        'deal_id': activity.activity_identifier,
        'history_id': activity.id,
        'user': user.username,
        'comment': activity.changeset_comment,
        'timestamp': history_date.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return template_data
