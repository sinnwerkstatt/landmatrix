# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0011_year_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('code_alpha2', models.CharField(verbose_name='Code ISO 3166-1 alpha2', max_length=2)),
                ('code_alpha3', models.CharField(verbose_name='Code ISO 3166-1 alpha3', max_length=3)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=100)),
                ('point_lat', models.DecimalField(decimal_places=12, null=True, verbose_name='Point lat', blank=True, max_digits=18)),
                ('point_lon', models.DecimalField(decimal_places=12, null=True, verbose_name='Point lon', blank=True, max_digits=18)),
                ('democracy_index', models.DecimalField(decimal_places=2, null=True, verbose_name='Democracy index', blank=True, max_digits=3)),
                ('corruption_perception_index', models.DecimalField(decimal_places=1, null=True, verbose_name='Corruption perception index', blank=True, max_digits=2)),
                ('high_income', models.BooleanField(verbose_name='High income')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('point_lat', models.DecimalField(decimal_places=12, null=True, verbose_name='Point lat', blank=True, max_digits=18)),
                ('point_lon', models.DecimalField(decimal_places=12, null=True, verbose_name='Point lon', blank=True, max_digits=18)),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='fk_region',
            field=models.ForeignKey(verbose_name='Region', to='landmatrix.Region'),
        ),
    ]
