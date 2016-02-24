# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='deals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('investor', models.CharField(max_length=200, verbose_name=b'Investor in Land')),
                ('target_country', models.CharField(max_length=100, verbose_name=b'Country of investment')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name': 'Deal',
                'verbose_name_plural': 'Deals',
            },
        ),
    ]
