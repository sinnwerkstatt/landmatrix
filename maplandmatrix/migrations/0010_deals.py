# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maplandmatrix', '0009_delete_deals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('deals_ID', models.CharField(max_length=50, null=True, verbose_name='Deals_ID', unique=True)),
                ('investor', models.CharField(verbose_name='Investor', max_length=200)),
                ('target_country', models.CharField(verbose_name='Country of investment', max_length=100)),
                ('deal_size', models.IntegerField(blank=True, null=True, verbose_name='Size in Hectare')),
                ('land_use', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Conservation', 'Conservation'), ('Forestry', 'Forestry'), ('Industry', 'Industry'), ('Mining', 'Mining'), ('Energy', 'Energy'), ('Tourism', 'Tourism'), ('Other', 'Other')], max_length=500, verbose_name='Intention of land use', default='Agriculture')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name': 'Deal',
                'verbose_name_plural': 'Deals',
            },
            bases=(models.Model,),
        ),
    ]
