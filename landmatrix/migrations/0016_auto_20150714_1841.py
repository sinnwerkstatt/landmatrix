# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0015_agriculturalproduce_crop'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('activity_identifier', 'version')]),
        ),
    ]
