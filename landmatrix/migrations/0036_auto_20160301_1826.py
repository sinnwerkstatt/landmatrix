# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0035_auto_20160209_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='fully_updated',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fully updated', null=True),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='fully_updated',
            field=models.DateTimeField(verbose_name='Fully updated', null=True, editable=False, blank=True),
        ),
    ]
