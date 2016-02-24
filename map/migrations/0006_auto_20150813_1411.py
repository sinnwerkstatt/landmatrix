# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20150806_0927'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WorldBorder',
        ),
        migrations.AddField(
            model_name='deals',
            name='deals_ID',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name=b'Deals_ID'),
        ),
        migrations.AlterField(
            model_name='deals',
            name='land_use',
            field=models.CharField(default=b'AG', max_length=500, verbose_name=b'Intention of land use', choices=[(b'AG', b'Agriculture'), (b'CONS', b'Conservation'), (b'FOR', b'Forestry'), (b'IND', b'Industry'), (b'MIN', b'Mining'), (b'EN', b'Energy'), (b'TR', b'Tourism'), (b'O', b'Other')]),
        ),
    ]
