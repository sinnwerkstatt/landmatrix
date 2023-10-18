from .models import FieldDefinition
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(FieldDefinition)
class FieldDefinitionTR(TranslationOptions):
    fields = ("short_description", "long_description", "editor_description")
