# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0053_auto_20160411_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('is', 'is'), ('in', 'in'), ('is_empty', 'is_empty'), ('gte', 'gte'), ('contains', 'contains'), ('gt', 'gt'), ('not_in', 'not_in'), ('lte', 'lte'), ('lt', 'lt')], max_length=10, verbose_name='Operator'),
        ),
    ]
