# Generated by Django 2.2.22 on 2021-06-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0031_auto_20210607_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealworkflowinfo',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
