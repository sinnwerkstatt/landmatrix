# Generated by Django 2.2.22 on 2021-06-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0035_auto_20210616_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='comment',
            field=models.TextField(blank=True, default='', help_text='A text comment on this revision.', verbose_name='comment'),
        ),
    ]
