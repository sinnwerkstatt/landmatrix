# Generated by Django 2.2.22 on 2021-06-07 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0030_dealworkflowinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealworkflowinfo',
            name='deal_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='landmatrix.DealVersion'),
        ),
    ]
