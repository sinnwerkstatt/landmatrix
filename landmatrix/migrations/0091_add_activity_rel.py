# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0090_ordering_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalactivity',
            name='public_version',
            field=models.OneToOneField(to='landmatrix.Activity', blank=True, null=True, related_name='historical_version'),
        ),
    ]
