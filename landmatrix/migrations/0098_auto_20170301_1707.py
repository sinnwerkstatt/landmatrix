# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.db import migrations, models
import jsonfield.fields


def load_geojson(apps, schema_editor):
    """
    Load geojson from git-repo
    """
    Country = apps.get_model('landmatrix', 'Country')
    db_alias = schema_editor.connection.alias
    countries = Country.objects.using(db_alias).iterator()
    geojson_base_url = 'https://raw.githubusercontent.com/mledoze/countries/master/data/{}.geo.json'
    for country in countries:
        response = requests.get(geojson_base_url.format(country.code_alpha3.lower()))
        try:
            country.polygon = response.json()['features'][0]['geometry']
        except Exception:
            print('\n no polygon for {} (id: {})'.format(country.name, country.id))
        country.save()


def purge_geojson(apps, schema_editor):
    Country = apps.get_model("landmatrix", "Country")
    db_alias = schema_editor.connection.alias
    Country.objects.using(db_alias).update(polygon=None)


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0097_updated_country_point_desc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalactivity',
            options={'get_latest_by': 'id', 'ordering': ('-history_date',), 'verbose_name_plural': 'Historical activities', 'verbose_name': 'Historical activity'},
        ),
        migrations.AddField(
            model_name='country',
            name='polygon',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.RunPython(load_geojson, purge_geojson)
    ]
