from django.db.models import Model, CharField, BooleanField
from django.utils.translation import ugettext_lazy as _


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterPreset(Model):
    group = CharField(_("Group"), max_length=255)
    name = CharField(_("Name"), max_length=255)
    is_default = BooleanField(default=False)
    overrides_default = BooleanField(default=False)

    def __str__(self):
        return self.group + ': ' + self.name

    def conditions(self):
        from landmatrix.models.filter_condition import FilterCondition
        return FilterCondition.objects.filter(fk_rule=self)

