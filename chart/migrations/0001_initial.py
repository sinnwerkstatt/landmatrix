# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetTheIdea',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='cms.CMSPlugin')),
                ('body', models.TextField(verbose_name='body', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
