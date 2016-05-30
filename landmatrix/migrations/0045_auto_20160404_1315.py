# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0044_auto_20160324_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='point_lat',
            new_name='point_lat_max',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='point_lon',
            new_name='point_lon_max',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='point_lat',
            new_name='point_lat_min',
        ),
        migrations.RemoveField(
            model_name='region',
            name='point_lon',
        ),
        migrations.AddField(
            model_name='country',
            name='point_lat_min',
            field=models.DecimalField(blank=True, max_digits=18, verbose_name='Point lat', decimal_places=12, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='point_lon_min',
            field=models.DecimalField(blank=True, max_digits=18, verbose_name='Point lon', decimal_places=12, null=True),
        ),
        migrations.AddField(
            model_name='region',
            name='point_lon_max',
            field=models.DecimalField(blank=True, max_digits=18, verbose_name='Point lon', decimal_places=12, null=True),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=10, choices=[('gte', 'gte'), ('gt', 'gt'), ('is_empty', 'is_empty'), ('not_in', 'not_in'), ('lte', 'lte'), ('is', 'is'), ('contains', 'contains'), ('lt', 'lt'), ('in', 'in')]),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='variable',
            field=models.CharField(verbose_name='Variable', max_length=32, choices=[('level_of_accuracy', 'Level Of Accuracy'), ('location', 'Location'), ('point_lat', 'Point Lat'), ('point_lon', 'Point Lon'), ('target_country', 'Target Country'), ('target_region', 'Target Region'), ('intended_size', 'Intended Size'), ('contract_size', 'Contract Size'), ('production_size', 'Production Size'), ('intention', 'Intention'), ('nature', 'Nature'), ('negotiation_status', 'Negotiation Status'), ('contract_number', 'Contract Number'), ('contract_date', 'Contract Date'), ('sold_as_deal', 'Sold As Deal'), ('agreement_duration', 'Agreement Duration'), ('implementation_status', 'Implementation Status'), ('purchase_price', 'Purchase Price'), ('purchase_price_currency', 'Purchase Price Currency'), ('purchase_price_type', 'Purchase Price Type'), ('purchase_price_area', 'Purchase Price Area'), ('annual_leasing_fee', 'Annual Leasing Fee'), ('annual_leasing_fee_currency', 'Annual Leasing Fee Currency'), ('annual_leasing_fee_type', 'Annual Leasing Fee Type'), ('annual_leasing_fee_area', 'Annual Leasing Fee Area'), ('contract_farming', 'Contract Farming'), ('on_the_lease', 'On The Lease'), ('on_the_lease_area', 'On The Lease Area'), ('on_the_lease_farmers', 'On The Lease Farmers'), ('off_the_lease', 'Off The Lease'), ('off_the_lease_area', 'Off The Lease Area'), ('off_the_lease_farmers', 'Off The Lease Farmers'), ('total_jobs_created', 'Total Jobs Created'), ('total_jobs_planned', 'Total Jobs Planned'), ('total_jobs_planned_employees', 'Total Jobs Planned Employees'), ('total_jobs_planned_daily_workers', 'Total Jobs Planned Daily Workers'), ('total_jobs_current', 'Total Jobs Current'), ('total_jobs_current_employees', 'Total Jobs Current Employees'), ('total_jobs_current_daily_workers', 'Total Jobs Current Daily Workers'), ('foreign_jobs_created', 'Foreign Jobs Created'), ('foreign_jobs_planned', 'Foreign Jobs Planned'), ('foreign_jobs_planned_employees', 'Foreign Jobs Planned Employees'), ('foreign_jobs_planned_daily_workers', 'Foreign Jobs Planned Daily Workers'), ('foreign_jobs_current', 'Foreign Jobs Current'), ('foreign_jobs_current_employees', 'Foreign Jobs Current Employees'), ('foreign_jobs_current_daily_workers', 'Foreign Jobs Current Daily Workers'), ('domestic_jobs_created', 'Domestic Jobs Created'), ('domestic_jobs_planned', 'Domestic Jobs Planned'), ('domestic_jobs_planned_employees', 'Domestic Jobs Planned Employees'), ('domestic_jobs_planned_daily_workers', 'Domestic Jobs Planned Daily Workers'), ('domestic_jobs_current', 'Domestic Jobs Current'), ('domestic_jobs_current_employees', 'Domestic Jobs Current Employees'), ('domestic_jobs_current_daily_workers', 'Domestic Jobs Current Daily Workers'), ('operational_stakeholder', 'Operational Stakeholder'), ('project_name', 'Project Name'), ('type', 'Type'), ('url', 'Url'), ('file', 'File'), ('date', 'Date'), ('name', 'Name'), ('company', 'Company'), ('email', 'Email'), ('phone', 'Phone'), ('includes_in_country_verified_information', 'Includes In Country Verified Information'), ('community_reaction', 'Community Reaction'), ('community_consultation', 'Community Consultation'), ('community_compensation', 'Community Compensation'), ('community_benefits', 'Community Benefits'), ('number_of_displaced_people', 'Number Of Displaced People'), ('land_owner', 'Land Owner'), ('land_use', 'Land Use'), ('land_cover', 'Land Cover'), ('crops', 'Crops'), ('animals', 'Animals'), ('minerals', 'Minerals'), ('has_domestic_use', 'Has Domestic Use'), ('domestic_use', 'Domestic Use'), ('has_export', 'Has Export'), ('export', 'Export'), ('export_country1', 'Export Country1'), ('export_country1_ratio', 'Export Country1 Ratio'), ('export_country2', 'Export Country2'), ('export_country2_ratioexport_country3', 'Export Country2 Ratioexport Country3'), ('export_country3_ratio', 'Export Country3 Ratio'), ('in_country_processing', 'In Country Processing'), ('water_extraction_envisaged', 'Water Extraction Envisaged'), ('source_of_water_extraction', 'Source Of Water Extraction'), ('water_extraction_amount', 'Water Extraction Amount'), ('fully_updated', 'Fully Updated'), ('fully_updated_history', 'Fully Updated History'), ('not_public', 'Not Public'), ('not_public_reason', 'Not Public Reason'), ('assign_to_user', 'Assign To User')]),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='implementation_status',
            field=models.CharField(blank=True, verbose_name='Implementation status', max_length=64, null=True, choices=[('', '---------'), ('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], db_index=True),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='negotiation_status',
            field=models.CharField(blank=True, verbose_name='Negotiation status', max_length=64, null=True, choices=[('', '---------'), ('Intended (Expression of interest)', 'Intended (Expression of interest)'), ('Intended (Under negotiation)', 'Intended (Under negotiation)'), ('Concluded (Oral Agreement)', 'Concluded (Oral Agreement)'), ('Concluded (Contract signed)', 'Concluded (Contract signed)'), ('Failed (Negotiations failed)', 'Failed (Negotiations failed)'), ('Failed (Contract canceled)', 'Failed (Contract canceled)'), ('Sold', 'Sold')], db_index=True),
        ),
    ]
