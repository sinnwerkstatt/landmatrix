# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0097_updated_country_point_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewdecision',
            name='description',
            field=models.TextField(verbose_name='Description', null=True, blank=True),
        ),
    ]
