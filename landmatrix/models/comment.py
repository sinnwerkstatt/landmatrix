
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(_("Comment"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    fk_user = models.ForeignKey(User, verbose_name=_("User"), blank=True, null=True)
    fk_activity = models.ForeignKey(
        "Activity", verbose_name=_("Activity"), blank=True, null=True
    )
    fk_activity_attribute_group = models.ForeignKey(
        "ActivityAttributeGroup", verbose_name=_("Activity attribute group"), blank=True, null=True
    )

    def __str__(self):
        return self.comment
