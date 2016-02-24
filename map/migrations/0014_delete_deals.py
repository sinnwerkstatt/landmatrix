# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_mappluginmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Deals',
        ),
    ]
