# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0013_auto_20150610_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowseCondition',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('variable', models.CharField(verbose_name='Variable', max_length=20)),
                ('operator', models.CharField(verbose_name='Operator', max_length=20)),
                ('value', models.CharField(verbose_name='Variable', max_length=1024)),
            ],
            options={
            },
            bases=(models.Model, landmatrix.models.default_string_representation.DefaultStringRepresentation),
        ),
        migrations.CreateModel(
            name='BrowseRule',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('rule_type', models.CharField(verbose_name='Rule type', choices=[('browse', 'Browse rule'), ('generic', 'Generic rule')], max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='browsecondition',
            name='rule',
            field=models.ForeignKey(to='landmatrix.BrowseRule'),
            preserve_default=True,
        ),
    ]
