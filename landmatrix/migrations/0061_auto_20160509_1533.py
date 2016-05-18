# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0060_auto_20160509_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('lte', 'lte'), ('in', 'in'), ('gt', 'gt'), ('is', 'is'), ('not_in', 'not_in'), ('lt', 'lt'), ('is_empty', 'is_empty'), ('contains', 'contains'), ('gte', 'gte')], verbose_name='Operator', max_length=10),
        ),
    ]
