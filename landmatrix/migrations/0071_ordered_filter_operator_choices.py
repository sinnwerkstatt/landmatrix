# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0070_auto_20160612_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', choices=[('is', 'is'), ('in', 'in'), ('not_in', 'not_in'), ('gte', 'gte'), ('gt', 'gt'), ('lte', 'lte'), ('lt', 'lt'), ('contains', 'contains'), ('is_empty', 'is_empty')], max_length=10),
        ),
    ]
