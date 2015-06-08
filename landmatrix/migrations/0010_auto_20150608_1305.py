# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0009_activityattributegroup_stakeholderattributegroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('english_name', models.CharField(verbose_name='English name', max_length=255)),
                ('local_name', models.CharField(verbose_name='Local name', max_length=255)),
                ('locale', models.CharField(verbose_name='Locale', max_length=31)),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.AddField(
            model_name='activityattributegroup',
            name='fk_language',
            field=models.ForeignKey(default=1, to='landmatrix.Language', verbose_name='Language'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stakeholderattributegroup',
            name='fk_language',
            field=models.ForeignKey(default=1, to='landmatrix.Language', verbose_name='Language'),
            preserve_default=False,
        ),
    ]
