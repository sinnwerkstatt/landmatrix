from django.db import models
from django.utils.translation import ugettext_lazy as _


class Crop(models.Model):

    fk_agricultural_produce = models.ForeignKey(
        "AgriculturalProduce", null=True, verbose_name=_("Agricultural produce"), on_delete=models.SET_NULL
    )
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug")

    def __str__(self):
        return self.name
