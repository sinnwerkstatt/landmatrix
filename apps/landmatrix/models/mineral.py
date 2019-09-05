
from django.db import models



class Mineral(models.Model):
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name
