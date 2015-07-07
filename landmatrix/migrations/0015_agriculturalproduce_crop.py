# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0014_auto_20150623_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgriculturalProduce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.CharField(verbose_name='Code', max_length=255)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('fk_agricultural_produce', models.ForeignKey(null=True, verbose_name='Agricultural produce', to='landmatrix.AgriculturalProduce')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
