# Generated by Django 2.2.22 on 2021-06-14 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0033_auto_20210608_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealworkflowinfo',
            name='deal_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landmatrix.DealVersion'),
        ),
    ]
