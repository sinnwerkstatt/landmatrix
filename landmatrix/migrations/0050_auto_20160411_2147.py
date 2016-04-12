# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0049_auto_20160411_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=10, choices=[('is', 'is'), ('lte', 'lte'), ('gte', 'gte'), ('contains', 'contains'), ('is_empty', 'is_empty'), ('in', 'in'), ('gt', 'gt'), ('not_in', 'not_in'), ('lt', 'lt')]),
        ),
    ]
