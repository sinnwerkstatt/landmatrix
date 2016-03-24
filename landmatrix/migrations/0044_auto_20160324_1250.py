# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0043_auto_20160324_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, verbose_name='Operator', choices=[('in', 'in'), ('gt', 'gt'), ('contains', 'contains'), ('gte', 'gte'), ('is_empty', 'is_empty'), ('lt', 'lt'), ('not_in', 'not_in'), ('lte', 'lte'), ('is', 'is')]),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='group',
            field=models.CharField(max_length=255, verbose_name='Group'),
        ),
    ]
