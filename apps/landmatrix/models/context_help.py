from django.db import models
from wagtail.snippets.models import register_snippet


@register_snippet
class ContextHelp(models.Model):
    identifier = models.CharField(unique=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"ContextHelp {self.identifier}"
