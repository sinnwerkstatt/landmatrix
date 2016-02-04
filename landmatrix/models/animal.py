from django.db import models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Animal(models.Model):
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name
