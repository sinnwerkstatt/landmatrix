# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_worldborders'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorldBorders',
            new_name='WorldBorder',
        ),
    ]
