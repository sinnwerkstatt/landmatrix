# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0042_auto_20160323_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterpreset',
            name='group',
            field=models.CharField(verbose_name='Name', max_length=255, default='Negotiation Status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('not_in', 'not_in'), ('in', 'in'), ('lt', 'lt'), ('is_empty', 'is_empty'), ('contains', 'contains'), ('is', 'is'), ('gt', 'gt'), ('lte', 'lte'), ('gte', 'gte')], verbose_name='Operator', max_length=10),
        ),
    ]
