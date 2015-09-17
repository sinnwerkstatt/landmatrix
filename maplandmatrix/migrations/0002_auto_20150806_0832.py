# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maplandmatrix', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals',
            name='deal_size',
            field=models.IntegerField(default=200, verbose_name=b'Size in Hectare'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deals',
            name='land_use',
            field=models.CharField(default='agriculture', max_length=500, verbose_name=b'Intention of land use'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deals',
            name='investor',
            field=models.CharField(max_length=200, verbose_name=b'Investor'),
        ),
    ]
