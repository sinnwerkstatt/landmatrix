from django.db import models


class FieldDefinition(models.Model):
    model = models.CharField(choices=(("deal", "Deal"), ("investor", "Investor")))
    field = models.CharField()
    short_description = models.TextField()
    long_description = models.TextField(blank=True)
    editor_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.model}: {self.field}"
