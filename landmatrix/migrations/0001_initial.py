# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-18 16:32
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import landmatrix.models.default_string_representation
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_identifier', models.IntegerField(db_index=True, verbose_name='Activity identifier')),
                ('availability', models.FloatField(blank=True, null=True, verbose_name='availability')),
                ('fully_updated', models.BooleanField(default=False, verbose_name='Fully updated')),
                ('is_public', models.BooleanField(db_index=True, default=False, verbose_name='Is this a public deal?')),
                ('deal_scope', models.CharField(blank=True, choices=[('domestic', 'Domestic'), ('domestic', 'Transnational')], db_index=True, max_length=16, null=True, verbose_name='Deal scope')),
                ('negotiation_status', models.CharField(blank=True, choices=[('', '---------'), ('Expression of interest', 'Intended (Expression of interest)'), ('Under negotiation', 'Intended (Under negotiation)'), ('Memorandum of understanding', 'Intended (Memorandum of understanding)'), ('Oral agreement', 'Concluded (Oral Agreement)'), ('Contract signed', 'Concluded (Contract signed)'), ('Negotiations failed', 'Failed (Negotiations failed)'), ('Contract canceled', 'Failed (Contract cancelled)'), ('Contract expired', 'Contract expired'), ('Change of ownership', 'Change of ownership')], db_index=True, max_length=64, null=True, verbose_name='Negotiation status')),
                ('implementation_status', models.CharField(blank=True, choices=[('', '---------'), ('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], db_index=True, max_length=64, null=True, verbose_name='Implementation status')),
                ('deal_size', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Deal size')),
                ('init_date', models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='Initiation year or date')),
            ],
            options={
                'permissions': (('review_activity', 'Can review activity changes'),),
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.TextField(blank=True, max_length=255, null=True)),
                ('value2', models.TextField(blank=True, max_length=255, null=True)),
                ('date', models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='Year or Date')),
                ('is_current', models.BooleanField(default=False, verbose_name='Is current')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('fk_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='landmatrix.Activity', verbose_name='Activity')),
            ],
            options={
                'verbose_name': 'Activity attribute',
                'verbose_name_plural': 'Activity attributes',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityAttributeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Activity attribute group',
                'verbose_name_plural': 'Activity attribute groups',
            },
        ),
        migrations.CreateModel(
            name='ActivityChangeset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='ActivityFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
            ],
            options={
                'verbose_name': 'Activity feedback',
                'ordering': ('-timestamp', '-id'),
                'verbose_name_plural': 'Activity feedbacks',
            },
        ),
        migrations.CreateModel(
            name='AgriculturalProduce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='BrowseCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=20, verbose_name='Variable')),
                ('operator', models.CharField(max_length=20, verbose_name='Operator')),
                ('value', models.CharField(max_length=1024, verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='BrowseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('rule_type', models.CharField(choices=[('browse', 'Browse rule'), ('generic', 'Generic rule')], max_length=255, verbose_name='Rule type')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('fk_activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Activity', verbose_name='Activity')),
                ('fk_activity_attribute_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity attribute group')),
                ('fk_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_alpha2', models.CharField(max_length=2, verbose_name='Code ISO 3166-1 alpha2')),
                ('code_alpha3', models.CharField(max_length=3, verbose_name='Code ISO 3166-1 alpha3')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('point_lat', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude of central point')),
                ('point_lon', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude of central point')),
                ('point_lat_min', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude of southernmost point')),
                ('point_lon_min', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude of westernmost point')),
                ('point_lat_max', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude of northernmost point')),
                ('point_lon_max', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude of easternmost point')),
                ('democracy_index', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Democracy index')),
                ('corruption_perception_index', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='Corruption perception index')),
                ('high_income', models.BooleanField(default=False, verbose_name='High income')),
                ('is_target_country', models.BooleanField(default=False, verbose_name='Is target country')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('fk_agricultural_produce', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.AgriculturalProduce', verbose_name='Agricultural produce')),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('symbol', models.CharField(max_length=255, verbose_name='Symbol')),
                ('country', models.CharField(max_length=2, verbose_name='Country')),
                ('ranking', models.IntegerField(verbose_name='Ranking')),
            ],
        ),
        migrations.CreateModel(
            name='FilterCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=32, verbose_name='Variable')),
                ('key', models.CharField(choices=[('value', 'Value'), ('value2', 'Value 2'), ('date', 'Date'), ('polygon', 'Polygon'), ('high_income', 'High income')], default='value', max_length=32, verbose_name='Key')),
                ('operator', models.CharField(choices=[('is', 'is'), ('in', 'in'), ('not_in', 'not_in'), ('gte', 'gte'), ('gt', 'gt'), ('lte', 'lte'), ('lt', 'lt'), ('contains', 'contains'), ('is_empty', 'is_empty')], max_length=10, verbose_name='Operator')),
                ('value', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='FilterPreset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('relation', models.CharField(choices=[('and', 'And'), ('or', 'Or')], default='and', max_length=3)),
                ('is_default_country', models.BooleanField(default=False, verbose_name='Country')),
                ('is_default_global', models.BooleanField(default=False, verbose_name='Global/Region')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Is hidden')),
            ],
            options={
                'verbose_name': 'Filter preset',
                'verbose_name_plural': 'Filter presets',
            },
        ),
        migrations.CreateModel(
            name='FilterPresetGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Filter preset group',
                'verbose_name_plural': 'Filter preset groups',
            },
        ),
        migrations.CreateModel(
            name='HistoricalActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_identifier', models.IntegerField(db_index=True, verbose_name='Activity identifier')),
                ('availability', models.FloatField(blank=True, null=True, verbose_name='availability')),
                ('fully_updated', models.BooleanField(default=False, verbose_name='Fully updated')),
                ('history_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
            ],
            options={
                'get_latest_by': 'id',
                'verbose_name': 'Historical activity',
                'ordering': ('-history_date',),
                'verbose_name_plural': 'Historical activities',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalActivityAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.TextField(blank=True, max_length=255, null=True)),
                ('value2', models.TextField(blank=True, max_length=255, null=True)),
                ('date', models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='Year or Date')),
                ('is_current', models.BooleanField(default=False, verbose_name='Is current')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('fk_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='landmatrix.HistoricalActivity', verbose_name='Activity')),
                ('fk_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity Attribute Group')),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'Historical activity attribute',
                'verbose_name_plural': 'Historical activity attributes',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInvestor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_identifier', models.IntegerField(db_index=True, default=2147483647, verbose_name='Investor id')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('classification', models.CharField(blank=True, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government (owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank (MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization (e.g. Church, University etc.)')], max_length=3, null=True)),
                ('parent_relation', models.CharField(blank=True, choices=[('Subsidiary', 'Subsidiary of parent company'), ('Local branch', 'Local branch of parent company'), ('Joint venture', 'Joint venture of parent companies')], max_length=255, null=True)),
                ('homepage', models.URLField(blank=True, null=True, verbose_name='Investor homepage')),
                ('opencorporates_link', models.URLField(blank=True, null=True, verbose_name='Opencorporates link')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('history_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('fk_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Country', verbose_name='Country of registration/origin')),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'Historical investor',
                'ordering': ['-history_date'],
                'verbose_name_plural': 'Historical investors',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_identifier', models.IntegerField(db_index=True, default=2147483647, verbose_name='Investor id')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('classification', models.CharField(blank=True, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government (owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank (MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization (e.g. Church, University etc.)')], max_length=3, null=True)),
                ('parent_relation', models.CharField(blank=True, choices=[('Subsidiary', 'Subsidiary of parent company'), ('Local branch', 'Local branch of parent company'), ('Joint venture', 'Joint venture of parent companies')], max_length=255, null=True)),
                ('homepage', models.URLField(blank=True, null=True, verbose_name='Investor homepage')),
                ('opencorporates_link', models.URLField(blank=True, null=True, verbose_name='Opencorporates link')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('fk_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Country', verbose_name='Country of registration/origin')),
            ],
            options={
                'verbose_name': 'Investor',
                'ordering': ('name',),
                'verbose_name_plural': 'Investors',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='InvestorActivityInvolvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('fk_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Activity', verbose_name='Activity')),
                ('fk_investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Investor', verbose_name='Investor')),
            ],
            options={
                'get_latest_by': 'timestamp',
                'verbose_name': 'Investor Activity Involvement',
                'ordering': ('-timestamp',),
                'verbose_name_plural': 'Investor Activity Involvements',
            },
        ),
        migrations.CreateModel(
            name='InvestorVentureInvolvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_type', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(10, 'Shares/Equity'), (20, 'Debt financing')], default='', max_length=255, null=True)),
                ('percentage', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Ownership share')),
                ('role', models.CharField(choices=[('ST', 'Stakeholder'), ('IN', 'Investor')], max_length=2)),
                ('loans_amount', models.FloatField(blank=True, null=True, verbose_name='Loan amount')),
                ('loans_date', models.CharField(blank=True, max_length=10, null=True, verbose_name='Loan date')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
                ('fk_investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='landmatrix.Investor')),
            ],
            options={
                'get_latest_by': 'timestamp',
                'verbose_name': 'Investor Venture Involvement',
                'ordering': ('-timestamp',),
                'verbose_name_plural': 'Investor Venture Involvements',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_name', models.CharField(max_length=255, verbose_name='English name')),
                ('local_name', models.CharField(max_length=255, verbose_name='Local name')),
                ('locale', models.CharField(max_length=31, verbose_name='Locale')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='Mineral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('point_lat_min', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude of northernmost point')),
                ('point_lon_min', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude of westernmost point')),
                ('point_lat_max', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude of southernmost point')),
                ('point_lon_max', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude of easternmost point')),
            ],
            bases=(models.Model, landmatrix.models.default_string_representation.DefaultStringRepresentation),
        ),
        migrations.CreateModel(
            name='ReviewDecision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='fk_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='fk_venture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venture_involvements', to='landmatrix.Investor'),
        ),
        migrations.AddField(
            model_name='investorventureinvolvement',
            name='loans_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Currency', verbose_name='Loan currency'),
        ),
        migrations.AddField(
            model_name='investoractivityinvolvement',
            name='fk_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='investor',
            name='fk_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='investor',
            name='subinvestors',
            field=models.ManyToManyField(through='landmatrix.InvestorVentureInvolvement', to='landmatrix.Investor'),
        ),
        migrations.AddField(
            model_name='historicalinvestor',
            name='fk_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='historicalinvestor',
            name='history_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='fk_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Language', verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='fk_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='history_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='public_version',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_version', to='landmatrix.Activity'),
        ),
        migrations.AddField(
            model_name='filterpreset',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_presets', to='landmatrix.FilterPresetGroup'),
        ),
        migrations.AddField(
            model_name='filtercondition',
            name='fk_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='landmatrix.FilterPreset'),
        ),
        migrations.AddField(
            model_name='country',
            name='fk_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='browsecondition',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.BrowseRule'),
        ),
        migrations.AddField(
            model_name='activityfeedback',
            name='fk_activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmatrix.HistoricalActivity', verbose_name='Activity'),
        ),
        migrations.AddField(
            model_name='activityfeedback',
            name='fk_user_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_assigned', to=settings.AUTH_USER_MODEL, verbose_name='User assigned'),
        ),
        migrations.AddField(
            model_name='activityfeedback',
            name='fk_user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created', to=settings.AUTH_USER_MODEL, verbose_name='User created'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changesets', to='landmatrix.HistoricalActivity', verbose_name='Activity'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Country', verbose_name='County'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_review_decision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.ReviewDecision', verbose_name='Review decision'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='activityattribute',
            name='fk_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity Attribute Group'),
        ),
        migrations.AddField(
            model_name='activityattribute',
            name='fk_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Language', verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='activity',
            name='fk_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AlterIndexTogether(
            name='activity',
            index_together=set([('is_public', 'deal_scope', 'negotiation_status', 'implementation_status'), ('is_public', 'deal_scope'), ('is_public', 'deal_scope', 'negotiation_status'), ('is_public', 'deal_scope', 'implementation_status')]),
        ),
    ]
