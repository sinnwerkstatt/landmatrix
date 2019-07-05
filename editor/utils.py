"""
Template rendering utils.

TODO: this can all be done in the template, move it there.
"""
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from grid.templatetags.custom_tags import get_user_role


def activity_or_investor_to_template(act_inv) -> dict:
    """
    Prepare activity/investor for template usage
    :param act_or_inv: activity or investor
    :return:
    """
    try:
        user = act_inv.history_user.username
        role = get_user_role(act_inv.history_user)
        if role:
            user += ' (%s)' % role
    except:
        # User doesn't exist anymore
        user = _('Deleted User')

    history_date = timezone.localtime(act_inv.history_date, timezone.get_current_timezone())

    is_activity = hasattr(act_inv, 'activity_identifier')
    if is_activity:
        id = act_inv.activity_identifier
    else:
        id = act_inv.investor_identifier

    return {
        'id': id,
        'history_id': act_inv.id,
        'user': user,
        'timestamp': history_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': act_inv.fk_status,
        'comment': act_inv.comment,
        'type': 'activity' if is_activity else 'investor',
    }


def feedback_to_template(feedback) -> dict:
    """
    Prepare feedback for template usage
    :param feedback:
    :return:
    """
    timestamp = timezone.localtime(
        feedback.timestamp, timezone.get_current_timezone())
    return {
        'id': feedback.fk_activity.activity_identifier,
        'history_id': feedback.fk_activity_id,
        'from_user': feedback.fk_user_created.username,
        'comment': feedback.comment,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    }


def reject_to_template(activity) -> dict:
    """
    Prepare reject for template usage
    :param activity:
    :return:
    """
    history_date = timezone.localtime(
        activity.history_date, timezone.get_current_timezone())
    user = activity.changesets.first().fk_user.username

    return {
        'deal_id': activity.activity_identifier,
        'history_id': activity.id,
        'user': user.username,
        'comment': activity.changeset_comment,
        'timestamp': history_date.strftime("%Y-%m-%d %H:%M:%S"),
    }
