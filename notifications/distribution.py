from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from editor.models import UserRegionalInfo
from landmatrix.models import Country, Region
from .models import NotificationEmail


User = get_user_model()
comment_notification_subject = _("landmatrix: A comment was posted")


def get_recipients_for_comment_on_activity(comment, activity):
    countries = Country.objects.get_target_countries_by_activity(activity)
    regions = Region.objects.get_target_regions_by_activity(activity)

    user_regions = UserRegionalInfo.objects.filter(country__in=countries) | \
        UserRegionalInfo.objects.filter(region__in=regions)

    recipients = User.objects.filter(userregionalinfo__in=user_regions)

    return recipients


def send_notifications_for_comment_on_activity(comment, request, activity,
                                               recipients):
    base_context = {
        'comment': comment,
        'request': request,
    }

    for recipient in recipients:
        context = base_context.copy()
        context['recipient'] = recipients

    NotificationEmail.objects.send(template_name='comment_posted',
                                   context=context,
                                   subject=comment_notification_subject,
                                   to=recipient.email)
