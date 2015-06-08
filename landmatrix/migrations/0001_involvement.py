# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Involvement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('investment_ratio', models.DecimalField(null=True, decimal_places=2, max_digits=19, blank=True, verbose_name='Investment ratio')),
            ],
        ),
    ]
