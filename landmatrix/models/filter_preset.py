from django.db import models
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.filter_condition import FilterCondition


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class FilterPresetGroup(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class FilterPreset(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    group = models.ForeignKey(FilterPresetGroup, related_name='filter_presets')
    is_default = models.BooleanField(default=False)
    overrides_default = models.BooleanField(default=False)

    def __str__(self):
        return self.group + ': ' + self.name

    def conditions(self):
        # TODO: why not just use self.filtercondition_set ?
        return FilterCondition.objects.filter(fk_rule=self)