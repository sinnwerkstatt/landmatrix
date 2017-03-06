# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models
import django.contrib.gis.db.models.fields


def load_country_geom(apps, schema_editor):
    call_command('load_country_geometries')


def purge_country_geom(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0097_updated_country_point_desc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalactivity',
            options={'get_latest_by': 'id', 'verbose_name_plural': 'Historical activities', 'ordering': ('-history_date',), 'verbose_name': 'Historical activity'},
        ),
        migrations.AddField(
            model_name='country',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
        migrations.RunPython(load_country_geom, purge_country_geom)
    ]
