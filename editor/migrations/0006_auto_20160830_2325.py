# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0005_userregionalinfo_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregionalinfo',
            name='country',
            field=models.ManyToManyField(blank=True, to='landmatrix.Country'),
        ),
        migrations.AlterField(
            model_name='userregionalinfo',
            name='region',
            field=models.ManyToManyField(blank=True, to='landmatrix.Region'),
        ),
    ]
