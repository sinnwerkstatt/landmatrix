# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0004_auto_20150604_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
    ]
