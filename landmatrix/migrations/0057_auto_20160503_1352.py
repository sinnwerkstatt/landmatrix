# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0056_auto_20160426_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinvestor',
            name='homepage',
            field=models.URLField(null=True, verbose_name='Investor homepage', blank=True),
        ),
        migrations.AddField(
            model_name='historicalinvestor',
            name='opencorporates_link',
            field=models.URLField(null=True, verbose_name='Opencorporates link', blank=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='homepage',
            field=models.URLField(null=True, verbose_name='Investor homepage', blank=True),
        ),
        migrations.AddField(
            model_name='investor',
            name='opencorporates_link',
            field=models.URLField(null=True, verbose_name='Opencorporates link', blank=True),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=models.CharField(choices=[('10', 'Shares/Equity'), ('20', 'Debt financing')], null=True, max_length=2, blank=True),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='loans_amount',
            field=models.FloatField(null=True, verbose_name='Loan amount', blank=True),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='loans_currency',
            field=models.ForeignKey(null=True, to='landmatrix.Currency', verbose_name='Loan curency', blank=True),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='lonas_date',
            field=models.DateField(null=True, verbose_name='Loan date', blank=True),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('lt', 'lt'), ('gte', 'gte'), ('in', 'in'), ('is', 'is'), ('is_empty', 'is_empty'), ('lte', 'lte'), ('contains', 'contains'), ('gt', 'gt'), ('not_in', 'not_in')], verbose_name='Operator', max_length=10),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='classification',
            field=models.CharField(choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government(owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank(MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund(all types incl.pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization(e.g.Church, University etc.)')], null=True, max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='classification',
            field=models.CharField(choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government(owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank(MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund(all types incl.pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization(e.g.Church, University etc.)')], null=True, max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='fk_country',
            field=models.ForeignKey(null=True, to='landmatrix.Country', verbose_name='Country of registration/origin', blank=True),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='percentage',
            field=models.FloatField(blank=True, null=True, verbose_name='Ownership share', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]
