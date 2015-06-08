# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0008_auto_20150608_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAttributeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField(blank=True, verbose_name='Year', null=True, db_index=True)),
                ('attributes', django_hstore.fields.DictionaryField(db_index=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('fk_activity', models.ForeignKey(verbose_name='Activity', to='landmatrix.Activity')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='StakeholderAttributeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attributes', django_hstore.fields.DictionaryField(db_index=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('fk_stakeholder', models.ForeignKey(verbose_name='Stakeholder', to='landmatrix.Stakeholder')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
    ]
