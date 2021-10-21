# Generated by Django 2.2.22 on 2021-08-18 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0042_auto_20210723_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='is_target_country',
        ),
        migrations.AlterField(
            model_name='investorworkflowinfo',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflowinfos', to='landmatrix.Investor'),
        ),
        migrations.AlterField(
            model_name='investorworkflowinfo',
            name='investor_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workflowinfos', to='landmatrix.InvestorVersion'),
        ),
    ]