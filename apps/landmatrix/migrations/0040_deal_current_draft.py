# Generated by Django 2.2.22 on 2021-07-16 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0039_auto_20210713_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='current_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landmatrix.DealVersion'),
        ),
    ]
