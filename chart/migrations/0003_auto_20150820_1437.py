# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('chart', '0002_animalplugin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animalplugin',
            name='animal',
        ),
        migrations.RemoveField(
            model_name='animalplugin',
            name='cmsplugin_ptr',
        ),
        migrations.DeleteModel(
            name='AnimalPlugin',
        ),
    ]
