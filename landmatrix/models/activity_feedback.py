from django.db.models import Model, AutoField, ForeignKey, TextField, DateTimeField, Manager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityFeedback(Model):

    class AFManager(Manager):

        def get_current_feedbacks(self, user_id):
            result = self.filter(fk_activity__fk_status__name__in=('active', 'overwritten')).\
                filter(fk_user_assigned_id=user_id).order_by('-timestamp')
            return result

    fk_activity = ForeignKey("Activity", verbose_name=_("Activity"))
    fk_user_assigned = ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User assigned"), related_name="user_assigned"
    )
    fk_user_created = ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User created"), related_name="user_created"
    )
    comment = TextField(_("Comment"))
    timestamp = DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = AFManager()

