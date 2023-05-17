from rest_framework import fields
from wagtail.rich_text import expand_db_html


class APIRichTextSerializer(fields.CharField):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return expand_db_html(representation)
