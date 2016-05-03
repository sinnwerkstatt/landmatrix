# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0057_auto_20160503_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('in', 'in'), ('gte', 'gte'), ('contains', 'contains'), ('gt', 'gt'), ('not_in', 'not_in'), ('lt', 'lt'), ('is', 'is'), ('lte', 'lte'), ('is_empty', 'is_empty')], verbose_name='Operator', max_length=10),
        ),
    ]
