from django.db.models import Model, CharField, BooleanField
from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterPreset(Model):
    name = CharField(_("Name"), max_length=255)
    is_default = BooleanField(default=False)
    overrides_default = BooleanField(default=False)

    def __str__(self):
        return self.name

