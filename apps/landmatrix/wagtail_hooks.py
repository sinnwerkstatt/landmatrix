from django import forms
from django.db.models import ForeignObjectRel
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from apps.landmatrix.models import FieldDefinition


class FieldDefinitionFieldSelect(forms.Select):
    @staticmethod
    def _get_choices():
        from apps.landmatrix.models.deal import Deal

        existing_fields = FieldDefinition.objects.values_list("field", flat=True)

        fields = []
        for field in Deal._meta.get_fields():
            if isinstance(field, ForeignObjectRel):
                continue

            name = str(field).rsplit(".", 1)[1]

            if str(name) in existing_fields:
                continue

            fields += [(name, name)]

        return fields

    def optgroups(self, name, value, attrs=None):
        self.choices = self._get_choices()
        return super().optgroups(name, value, attrs=attrs)


class FieldDefinitionViewSet(SnippetViewSet):
    model = FieldDefinition

    panels = [
        FieldPanel("model"),
        FieldPanel("field", widget=FieldDefinitionFieldSelect),
        FieldPanel("short_description"),
        FieldPanel("long_description"),
        FieldPanel("editor_description"),
    ]


register_snippet(FieldDefinitionViewSet)
