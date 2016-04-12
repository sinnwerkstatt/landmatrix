# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0052_auto_20160411_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('not_in', 'not_in'), ('gt', 'gt'), ('is', 'is'), ('lt', 'lt'), ('is_empty', 'is_empty'), ('contains', 'contains'), ('gte', 'gte'), ('in', 'in'), ('lte', 'lte')], verbose_name='Operator', max_length=10),
        ),
    ]
