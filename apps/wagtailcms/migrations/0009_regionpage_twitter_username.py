# Generated by Django 2.2.16 on 2020-10-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0008_auto_20201013_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionpage',
            name='twitter_username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
