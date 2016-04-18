# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0054_auto_20160411_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='is_target_country',
            field=models.BooleanField(default=False, verbose_name='Is target country'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('contains', 'contains'), ('in', 'in'), ('gte', 'gte'), ('not_in', 'not_in'), ('lt', 'lt'), ('lte', 'lte'), ('gt', 'gt'), ('is', 'is'), ('is_empty', 'is_empty')], max_length=10, verbose_name='Operator'),
        ),
    ]
