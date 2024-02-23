from django import forms
from django.db import models
from django.db.models import ForeignObjectRel
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class _FieldDefinitionFieldSelect(forms.Select):
    @staticmethod
    def _get_choices(current_choices: list[str] = None):
        from apps.landmatrix.models.deal import DealOld

        existing_fields = FieldDefinition.objects.exclude(
            field__in=current_choices
        ).values_list("field", flat=True)

        fields = []
        for field in DealOld._meta.get_fields():
            if isinstance(field, ForeignObjectRel):
                continue

            name = str(field).rsplit(".", 1)[1]

            if str(name) in existing_fields:
                continue

            fields += [(name, name)]

        return fields

    def optgroups(self, name, value, attrs=None):
        self.choices = self._get_choices(value)
        return super().optgroups(name, value, attrs=attrs)


class FieldDefinition(models.Model):
    model = models.CharField(choices=(("deal", "Deal"), ("investor", "Investor")))
    field = models.CharField()
    short_description = models.TextField()
    long_description = models.TextField(blank=True)
    editor_description = models.TextField(blank=True)

    panels = [
        FieldPanel("model"),
        FieldPanel("field", widget=_FieldDefinitionFieldSelect),
        FieldPanel("short_description"),
        FieldPanel("long_description"),
        FieldPanel("editor_description"),
    ]

    def __str__(self):
        return f"{self.model}: {self.field}"


register_snippet(FieldDefinition)
