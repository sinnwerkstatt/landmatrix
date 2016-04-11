# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0050_auto_20160411_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('lte', 'lte'), ('contains', 'contains'), ('gte', 'gte'), ('is_empty', 'is_empty'), ('is', 'is'), ('lt', 'lt'), ('gt', 'gt'), ('not_in', 'not_in'), ('in', 'in')], max_length=10, verbose_name='Operator'),
        ),
    ]
