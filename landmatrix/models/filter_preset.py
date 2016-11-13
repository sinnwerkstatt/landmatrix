from django.db import models
from django.utils.translation import ugettext_lazy as _




class FilterPresetGroup(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter preset group')
        verbose_name_plural = _('Filter preset groups')


class FilterPreset(models.Model):
    RELATION_AND = 'and'
    RELATION_OR = 'or'
    RELATION_CHOICES = (
        (RELATION_AND, _('And')),
        (RELATION_OR, _('Or')),
    )

    name = models.CharField(_("Name"), max_length=255)
    group = models.ForeignKey(FilterPresetGroup, related_name='filter_presets',
                              null=True)
    relation = models.CharField(max_length=3, choices=RELATION_CHOICES,
                                default=RELATION_AND)
    is_default_country_region = models.BooleanField(_("Country/Region"), default=False)
    is_default_global = models.BooleanField(_("Global"), default=False)
    is_hidden = models.BooleanField(_("Is hidden"), default=False)

    def __str__(self):
        return '{}: {}'.format(self.group, self.name)

    class Meta:
        verbose_name = _('Filter preset')
        verbose_name_plural = _('Filter presets')