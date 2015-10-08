# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0016_auto_20150714_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=3, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('symbol', models.CharField(max_length=255, verbose_name='Symbol')),
                ('country', models.CharField(max_length=2, verbose_name='Country')),
                ('ranking', models.IntegerField(verbose_name='Ranking')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
