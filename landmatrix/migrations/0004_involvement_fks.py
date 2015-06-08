# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0003_primaryinvestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='involvement',
            name='fk_activity',
            field=models.ForeignKey(verbose_name='Activity', blank=True, to='landmatrix.Activity', null=True),
        ),
        migrations.AddField(
            model_name='involvement',
            name='fk_primary_investor',
            field=models.ForeignKey(verbose_name='Is primary', blank=True, to='landmatrix.PrimaryInvestor', null=True),
        ),
        migrations.AddField(
            model_name='involvement',
            name='fk_stakeholder',
            field=models.ForeignKey(verbose_name='Stakeholder', blank=True, to='landmatrix.Stakeholder', null=True),
        ),
    ]
