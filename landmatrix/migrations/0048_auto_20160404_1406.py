# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0047_auto_20160404_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, choices=[('is', 'is'), ('gt', 'gt'), ('contains', 'contains'), ('is_empty', 'is_empty'), ('lt', 'lt'), ('in', 'in'), ('lte', 'lte'), ('gte', 'gte'), ('not_in', 'not_in')], verbose_name='Operator'),
        ),
    ]
