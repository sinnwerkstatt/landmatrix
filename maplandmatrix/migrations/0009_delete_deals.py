# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maplandmatrix', '0008_auto_20150813_1421'),
    ]

    operations = [
        migrations.DeleteModel(
            name='deals',
        ),
    ]
