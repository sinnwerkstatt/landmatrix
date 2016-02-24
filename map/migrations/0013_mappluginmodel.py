# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('map', '0010_deals'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='cms.CMSPlugin', serialize=False, auto_created=True)),
                ('body', models.TextField(blank=True, null=True, verbose_name='body')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
