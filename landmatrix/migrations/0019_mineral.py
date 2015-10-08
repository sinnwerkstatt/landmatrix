# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0018_auto_20150803_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mineral',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
