from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from apps.landmatrix.models.field_definition import FieldDefinition


@register(FieldDefinition)
class FieldDefinitionTR(TranslationOptions):
    fields = ("short_description", "long_description", "editor_description")
