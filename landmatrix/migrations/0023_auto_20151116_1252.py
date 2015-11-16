# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0022_auto_20151116_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='investoractivityinvolvement',
            name='comment',
            field=models.TextField(null=True, blank=True, verbose_name='Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='comment',
            field=models.TextField(null=True, blank=True, verbose_name='Comment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='investor',
            name='comment',
            field=models.TextField(null=True, blank=True, verbose_name='Comment'),
            preserve_default=True,
        ),
    ]
