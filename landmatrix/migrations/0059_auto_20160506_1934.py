# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0058_auto_20160503_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('lte', 'lte'), ('contains', 'contains'), ('gt', 'gt'), ('in', 'in'), ('is', 'is'), ('lt', 'lt'), ('not_in', 'not_in'), ('gte', 'gte'), ('is_empty', 'is_empty')], max_length=10, verbose_name='Operator'),
        ),
    ]
