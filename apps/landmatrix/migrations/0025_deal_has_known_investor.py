# Generated by Django 2.2.17 on 2021-03-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0024_auto_20210324_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='has_known_investor',
            field=models.BooleanField(default=False),
        ),
    ]
