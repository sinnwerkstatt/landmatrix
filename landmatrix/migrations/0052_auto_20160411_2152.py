# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0051_auto_20160411_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', choices=[('not_in', 'not_in'), ('lt', 'lt'), ('gt', 'gt'), ('is_empty', 'is_empty'), ('lte', 'lte'), ('is', 'is'), ('contains', 'contains'), ('gte', 'gte'), ('in', 'in')], max_length=10),
        ),
    ]
