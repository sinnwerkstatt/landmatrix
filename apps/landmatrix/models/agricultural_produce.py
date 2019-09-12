
from django.db import models


class AgriculturalProduce(models.Model):
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name
