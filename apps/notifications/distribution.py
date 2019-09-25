from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from apps.editor.models import UserRegionalInfo
from .models import NotificationEmail

User = get_user_model()
comment_notification_subject = _("Land Matrix: New comment")


def get_recipients_for_comment_on_activity(comment, activity):
    # Add users assigned to target country or region
    recipients = UserRegionalInfo.objects.filter(
        Q(country=activity.target_country) | Q(region=activity.target_country.fk_region)
    )
    recipients = [u.user.email for u in recipients]
    # Add author of original comment (if reply)
    if comment.parent:
        if comment.parent.user:
            recipients.append(comment.parent.user.email)
        else:
            recipients.append(comment.parent.user_email)
    return set(filter(None, recipients))


def send_notifications_for_comment_on_activity(comment, request, activity):
    context = {"comment": comment, "request": request}
    recipients = get_recipients_for_comment_on_activity(comment, activity)
    for recipient in recipients:
        NotificationEmail.objects.send(
            template_name="comment_posted",
            context=context,
            subject=comment_notification_subject,
            to=recipient,
        )
