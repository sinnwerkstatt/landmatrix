from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.api.filters import FILTER_OPERATION_MAP, Filter


class FilterCondition(models.Model):
    OPERATOR_CHOICES = ((key, key) for key in FILTER_OPERATION_MAP.keys())
    KEY_CHOICE_VALUE = 'value'
    KEY_CHOICE_VALUE2 = 'value2'
    KEY_CHOICE_DATE = 'date'
    KEY_CHOICE_POLYGON = 'polygon'
    KEY_CHOICE_HIGH_INCOME = 'high_income'
    KEY_CHOICES = (
        (KEY_CHOICE_VALUE, _('Value')),
        (KEY_CHOICE_VALUE2, _('Value 2')),
        (KEY_CHOICE_DATE, _('Date')),
        (KEY_CHOICE_POLYGON, _('Polygon')),
        (KEY_CHOICE_HIGH_INCOME, _('High income')),
    )

    fk_rule = models.ForeignKey('landmatrix.FilterPreset', related_name='conditions', on_delete=models.CASCADE)
    variable = models.CharField(_("Variable"), max_length=32)
    key = models.CharField(_("Key"), choices=KEY_CHOICES, max_length=32, default=KEY_CHOICE_VALUE)
    operator = models.CharField(_("Operator"), max_length=20, choices=OPERATOR_CHOICES)
    value = models.CharField(_("Value"), max_length=1024, null=True, blank=True)

    def __str__(self):
        return '{}.{} {} {}'.format(self.variable, self.key, self.operator, self.value)

    def to_filter(self):
        return Filter(self.variable, self.operator, self.parsed_value, label=str(self), key=self.key)

    @property
    def parsed_value(self):
        if ',' in self.value:
            return [v.strip() for v in self.value.split(',')]
        return self.value


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
    group = models.ForeignKey(FilterPresetGroup, related_name='filter_presets', null=True, on_delete=models.SET_NULL)
    relation = models.CharField(max_length=3, choices=RELATION_CHOICES, default=RELATION_AND)
    is_default_country = models.BooleanField(_("Country"), default=False)
    is_default_global = models.BooleanField(_("Global/Region"), default=False)
    is_hidden = models.BooleanField(_("Is hidden"), default=False)

    def __str__(self):
        return '{}: {}'.format(self.group, self.name)

    class Meta:
        verbose_name = _('Filter preset')
        verbose_name_plural = _('Filter presets')
