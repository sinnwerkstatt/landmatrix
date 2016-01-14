# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0021_investor_investoractivityinvolvement_investorventureinvolvement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investor',
            old_name='country',
            new_name='fk_country',
        ),
        migrations.RenameField(
            model_name='investoractivityinvolvement',
            old_name='activity',
            new_name='fk_activity',
        ),
        migrations.RenameField(
            model_name='investoractivityinvolvement',
            old_name='investor',
            new_name='fk_investor',
        ),
        migrations.RenameField(
            model_name='investorventureinvolvement',
            old_name='investor',
            new_name='fk_investor',
        ),
        migrations.RenameField(
            model_name='investorventureinvolvement',
            old_name='venture',
            new_name='fk_venture',
        ),
    ]
