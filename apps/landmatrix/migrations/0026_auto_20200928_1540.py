# Generated by Django 2.2.14 on 2020-09-28 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0025_auto_20200830_0941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datasource',
            options={'ordering': ['date']},
        ),
    ]