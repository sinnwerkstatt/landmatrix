# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0019_mineral'),
        ('cms', '0012_auto_20150607_2207'),
        ('chart_view', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='cms.CMSPlugin', parent_link=True, serialize=False)),
                ('animal', models.ForeignKey(to='landmatrix.Animal')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
