# Generated by Django 5.0.10 on 2024-12-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0031_investorqisnapshot_dealqisnapshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContextHelp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
            ],
        ),
    ]
