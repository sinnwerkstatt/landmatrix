# Generated by Django 2.2.13 on 2020-06-19 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greennewdeal', '0009_auto_20200619_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='target_country',
            new_name='country',
        ),
    ]