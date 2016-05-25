# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0063_auto_20160522_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filterpreset',
            name='old_group',
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=10, choices=[('gte', 'gte'), ('lt', 'lt'), ('is_empty', 'is_empty'), ('contains', 'contains'), ('not_in', 'not_in'), ('gt', 'gt'), ('in', 'in'), ('is', 'is'), ('lte', 'lte')]),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='group',
            field=models.ForeignKey(null=True, related_name='filter_presets', to='landmatrix.FilterPresetGroup'),
        ),
    ]
