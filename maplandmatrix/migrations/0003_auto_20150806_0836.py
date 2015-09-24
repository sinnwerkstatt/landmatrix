# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maplandmatrix', '0002_auto_20150806_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deals',
            name='deal_size',
            field=models.IntegerField(default=200, verbose_name=b'Size in Hectare', blank=True),
        ),
    ]
