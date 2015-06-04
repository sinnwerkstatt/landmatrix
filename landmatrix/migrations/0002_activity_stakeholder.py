# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('activity_identifier', models.IntegerField(db_index=True, verbose_name='Activity identifier')),
                ('version', models.IntegerField(db_index=True, verbose_name='Version')),
                ('availability', models.FloatField(blank=True, verbose_name='availability', null=True)),
                ('fully_updated', models.DateTimeField(blank=True, verbose_name='Fully updated', null=True)),
            ],
            bases=(landmatrix.models.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stakeholder_identifier', models.IntegerField(db_index=True, verbose_name='Stakeholder id')),
                ('version', models.IntegerField(db_index=True, verbose_name='Version')),
            ],
        ),
    ]
