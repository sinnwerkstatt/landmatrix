# Generated by Django 4.2.6 on 2023-10-18 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0010_alter_fielddefinition_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='fielddefinition',
            name='editor_description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='editor_description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='editor_description_fr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='editor_description_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='long_description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='long_description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='long_description_fr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='long_description_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='short_description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='short_description_es',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='short_description_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='short_description_ru',
            field=models.TextField(null=True),
        ),
    ]
