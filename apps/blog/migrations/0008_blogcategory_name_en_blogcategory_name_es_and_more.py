# Generated by Django 5.0.3 on 2024-03-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_blogpage_body_en_remove_blogpage_body_es_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='name_en',
            field=models.CharField(null=True, unique=True, verbose_name='Category Name'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='name_es',
            field=models.CharField(null=True, unique=True, verbose_name='Category Name'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='name_fr',
            field=models.CharField(null=True, unique=True, verbose_name='Category Name'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='name_ru',
            field=models.CharField(null=True, unique=True, verbose_name='Category Name'),
        ),
    ]
