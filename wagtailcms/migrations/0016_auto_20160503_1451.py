# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0015_auto_20160503_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country',
            field=models.ForeignKey(blank=True, to='landmatrix.Country', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='region',
            name='region',
            field=models.ForeignKey(blank=True, to='landmatrix.Region', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
