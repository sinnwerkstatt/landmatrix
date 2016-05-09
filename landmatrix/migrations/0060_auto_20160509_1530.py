# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0059_auto_20160506_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, choices=[('lt', 'lt'), ('in', 'in'), ('not_in', 'not_in'), ('is', 'is'), ('gt', 'gt'), ('lte', 'lte'), ('gte', 'gte'), ('is_empty', 'is_empty'), ('contains', 'contains')], verbose_name='Operator'),
        ),
    ]
