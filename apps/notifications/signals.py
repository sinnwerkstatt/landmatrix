from django.dispatch import receiver
from django_comments.signals import comment_was_posted

from apps.landmatrix.models.activity import Activity
from .distribution import send_notifications_for_comment_on_activity


@receiver(comment_was_posted, dispatch_uid='comment_on_activity_posted')
def handle_comment_on_activity_posted(comment, request, **kwargs):
    """
    If we get a new comment, check that it was on an activity, and if so
    send any notifications required.
    """
    activity = comment.content_object
    if isinstance(activity, Activity):
        send_notifications_for_comment_on_activity(comment, request, activity)
