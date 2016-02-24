# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_auto_20150813_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deals',
            name='deal_size',
            field=models.IntegerField(null=True, verbose_name=b'Size in Hectare', blank=True),
        ),
    ]
