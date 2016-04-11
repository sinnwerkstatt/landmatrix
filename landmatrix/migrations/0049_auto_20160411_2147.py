# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0048_auto_20160404_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('is', 'is'), ('gte', 'gte'), ('lte', 'lte'), ('in', 'in'), ('not_in', 'not_in'), ('is_empty', 'is_empty'), ('gt', 'gt'), ('lt', 'lt'), ('contains', 'contains')], verbose_name='Operator', max_length=10),
        ),
    ]
