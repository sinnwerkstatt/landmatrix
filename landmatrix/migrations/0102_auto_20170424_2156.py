# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0101_auto_20170404_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='init_date',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Initiation year or date', db_index=True),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='is_default_country',
            field=models.BooleanField(verbose_name='Country', default=False),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='is_default_global',
            field=models.BooleanField(verbose_name='Global/Region', default=False),
        ),
    ]
