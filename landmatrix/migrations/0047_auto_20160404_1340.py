# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0046_auto_20160404_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=10, choices=[('lt', 'lt'), ('gte', 'gte'), ('in', 'in'), ('gt', 'gt'), ('contains', 'contains'), ('is_empty', 'is_empty'), ('lte', 'lte'), ('is', 'is'), ('not_in', 'not_in')]),
        ),
    ]
