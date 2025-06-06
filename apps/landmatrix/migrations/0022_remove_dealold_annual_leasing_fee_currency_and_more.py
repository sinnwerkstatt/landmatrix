# Generated by Django 5.0.4 on 2024-07-11 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0021_area_nid_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealold',
            name='annual_leasing_fee_currency',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='country',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='current_draft',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='export_country1',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='export_country2',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='export_country3',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='operating_company',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='parent_companies',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='purchase_price_currency',
        ),
        migrations.RemoveField(
            model_name='dealold',
            name='top_investors',
        ),
        migrations.RemoveField(
            model_name='dealworkflowinfoold',
            name='deal',
        ),
        migrations.RemoveField(
            model_name='dealversionold',
            name='object',
        ),
        migrations.RemoveField(
            model_name='dealversionold',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='dealversionold',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='dealworkflowinfoold',
            name='deal_version',
        ),
        migrations.RemoveField(
            model_name='dealworkflowinfoold',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='dealworkflowinfoold',
            name='to_user',
        ),
        migrations.RemoveField(
            model_name='investorold',
            name='country',
        ),
        migrations.RemoveField(
            model_name='investorold',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='investorold',
            name='current_draft',
        ),
        migrations.RemoveField(
            model_name='investorold',
            name='involvements',
        ),
        migrations.RemoveField(
            model_name='investorold',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='investorversionold',
            name='object',
        ),
        migrations.RemoveField(
            model_name='investorventureinvolvement',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='investorworkflowinfoold',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='investorventureinvolvement',
            name='venture',
        ),
        migrations.RemoveField(
            model_name='investorventureinvolvement',
            name='loans_currency',
        ),
        migrations.RemoveField(
            model_name='investorversionold',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='investorversionold',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='investorworkflowinfoold',
            name='investor_version',
        ),
        migrations.RemoveField(
            model_name='investorworkflowinfoold',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='investorworkflowinfoold',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='DealOldParentCompanies',
        ),
        migrations.DeleteModel(
            name='DealOldTopInvestors',
        ),
        migrations.DeleteModel(
            name='DealOld',
        ),
        migrations.DeleteModel(
            name='DealVersionOld',
        ),
        migrations.DeleteModel(
            name='DealWorkflowInfoOld',
        ),
        migrations.DeleteModel(
            name='InvestorOld',
        ),
        migrations.DeleteModel(
            name='InvestorVentureInvolvement',
        ),
        migrations.DeleteModel(
            name='InvestorVersionOld',
        ),
        migrations.DeleteModel(
            name='InvestorWorkflowInfoOld',
        ),
    ]
