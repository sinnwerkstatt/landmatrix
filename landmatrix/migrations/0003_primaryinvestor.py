# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0002_activity_stakeholder'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryInvestor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('primary_investor_identifier', models.IntegerField(db_index=True, verbose_name='Primary investor id')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('version', models.IntegerField(db_index=True, verbose_name='Version')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='id',
            field=models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID'),
        ),
    ]
