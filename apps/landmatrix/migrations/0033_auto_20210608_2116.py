# Generated by Django 2.2.22 on 2021-06-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0032_auto_20210608_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='confidential_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comment why this deal is private'),
        ),
    ]
