# Generated by Django 3.2.7 on 2021-09-29 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0047_auto_20210826_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='prai_applied',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='prai_applied_comment',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='vggt_applied',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='vggt_applied_comment',
        ),
    ]
