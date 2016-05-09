# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0061_auto_20160509_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', choices=[('is_empty', 'is_empty'), ('in', 'in'), ('lt', 'lt'), ('is', 'is'), ('gt', 'gt'), ('lte', 'lte'), ('gte', 'gte'), ('not_in', 'not_in'), ('contains', 'contains')], max_length=10),
        ),
    ]
