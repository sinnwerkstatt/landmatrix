from django.db.models import Model, AutoField, ForeignKey, TextField, DateTimeField, Manager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityFeedback(Model):

    class AFManager(Manager):
        def get_current_feedbacks(self, user_id):
            result = self.filter(fk_activity__fk_status__name__in=('active', 'overwritten')).filter(fk_user_assigned=user_id)
            # result = self.raw("""
            #     SELECT
            #         f.*
            #       FROM
            #         a_feedbacks f,
            #         activities a,
            #         status s
            #       WHERE
            #        f.fk_activity = a.id
            #        AND a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            #        AND a.fk_status = s.id
            #        AND s.name IN ("active", "overwritten")
            #        AND f.fk_user_assigned = %s
            #       ORDER BY f.timestamp DESC
            # """ % user_id)
            return list(result)

    id = AutoField(primary_key=True)
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

