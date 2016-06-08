# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0068_auto_20160531_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investorventureinvolvement',
            old_name='lonas_date',
            new_name='loans_date',
        ),
        migrations.AddField(
            model_name='investor',
            name='subinvestors',
            field=models.ManyToManyField(to='landmatrix.Investor', through='landmatrix.InvestorVentureInvolvement'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, verbose_name='Operator', choices=[('is', 'is'), ('in', 'in'), ('not_in', 'not_in'), ('gte', 'gte'), ('gt', 'gt'), ('lte', 'lte'), ('lt', 'lt'), ('contains', 'contains'), ('is_empty', 'is_empty')]),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='fk_venture',
            field=models.ForeignKey(related_name='venture_involvements', to='landmatrix.Investor'),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=models.CharField(max_length=2, null=True, blank=True, choices=[(10, 'Shares/Equity'), (20, 'Debt financing')]),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='is_deal',
            field=models.BooleanField(verbose_name='Is this a public deal?', db_index=True, default=False),
        ),
    ]
