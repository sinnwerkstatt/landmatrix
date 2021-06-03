# Generated by Django 2.2.22 on 2021-06-03 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0029_reset_id_seq'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealWorkflowInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draft_status_before', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('draft_status_after', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('processed_by_receiver', models.BooleanField(default=False)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='landmatrix.Deal')),
                ('deal_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='landmatrix.DealVersion')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
