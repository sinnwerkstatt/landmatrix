# Generated by Django 5.0.4 on 2024-09-04 09:22

import apps.landmatrix.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountability', '0010_vggtvariable_score_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='vggtvariable',
            name='articles',
            field=models.ManyToManyField(related_name='variables', to='accountability.vggtarticle'),
        ),
        migrations.AlterField(
            model_name='vggtvariable',
            name='score_options',
            field=apps.landmatrix.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('NO_DATA', 'Insufficient data'), ('SEVERE_VIOLATIONS', 'Severe violations'), ('PARTIAL_VIOLATIONS', 'Violations'), ('NO_VIOLATIONS', 'No violation')]), blank=True, default=['NO_DATA', 'SEVERE_VIOLATIONS', 'PARTIAL_VIOLATIONS', 'NO_VIOLATIONS'], size=None),
        ),
    ]
