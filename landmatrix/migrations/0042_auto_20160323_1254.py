# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0041_filtercondition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filtercondition',
            old_name='rule',
            new_name='fk_rule',
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('gt', 'gt'), ('lt', 'lt'), ('not_in', 'not_in'), ('in', 'in'), ('contains', 'contains'), ('gte', 'gte'), ('is', 'is'), ('lte', 'lte'), ('is_empty', 'is_empty')], max_length=10, verbose_name='Operator'),
        ),
    ]
