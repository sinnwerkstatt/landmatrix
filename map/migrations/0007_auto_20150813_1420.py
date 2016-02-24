# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0006_auto_20150813_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deals',
            name='land_use',
            field=models.CharField(default=b'Agriculture', max_length=500, verbose_name=b'Intention of land use', choices=[(b'Agriculture', b'Agriculture'), (b'Conservation', b'Conservation'), (b'Forestry', b'Forestry'), (b'Industry', b'Industry'), (b'Mining', b'Mining'), (b'Energy', b'Energy'), (b'Tourism', b'Tourism'), (b'Other', b'Other')]),
        ),
    ]
