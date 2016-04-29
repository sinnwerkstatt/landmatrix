from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from threadedcomments.models import ThreadedComment

from .models import NotificationEmail


@receiver(post_save, sender=ThreadedComment, dispatch_uid='comment_saved')
def handle_comment_saved(sender, instance, created, **kwargs):
    '''
    TODO: This is not really complete yet. It needs to properly figure out
    who should recieve notifications, and maybe should fire on comment will be
    posted instead (not sure if we're using moderation).
    '''
    context = {
        'comment': instance,
    }
    subject = _("landmatrix: A comment was posted")
    to = 'test@example.com'  # TODO: real to email

    NotificationEmail.objects.send(template_name='comment_posted',
                                   context=context, subject=subject, to=to)
