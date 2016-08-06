from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.db.models import Q

from editor.models import UserRegionalInfo
from landmatrix.models.country import Country
from landmatrix.models.region import Region
from .models import NotificationEmail


User = get_user_model()
comment_notification_subject = _("Land Matrix: A comment was posted")


def get_recipients_for_comment_on_activity(comment, activity):
    # Add users assigned to target country or region
    recipients = UserRegionalInfo.objects.filter(Q(country=activity.target_country) | \
        Q(region=activity.target_country.fk_region))
    recipients = [u.user.email for u in recipients]
    # Add author of original comment (if reply)
    print("A")
    print(dir(comment))
    if comment.parent:
        print("B")
        recipients.append(comment.parent.user.email)
    return recipients

def send_notifications_for_comment_on_activity(comment, request, activity):
    context = {
        'comment': comment,
        'request': request,
    }
    recipients = get_recipients_for_comment_on_activity(comment, activity)
    print(recipients)
    for recipient in filter(None, recipients):
      NotificationEmail.objects.send(template_name='comment_posted',
                                     context=context,
                                     subject=comment_notification_subject,
                                     to=recipient)
