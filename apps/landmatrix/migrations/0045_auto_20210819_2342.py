# Generated by Django 2.2.22 on 2021-08-19 21:42

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0044_purge_version_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, help_text='The date and time this revision was created.', verbose_name='date created')),
                ('serialized_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_by', models.ForeignKey(blank=True, help_text='The user who created this revision.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='versions', to='landmatrix.Deal')),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealWorkflowInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draft_status_before', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('draft_status_after', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True, null=True)),
                ('processed_by_receiver', models.BooleanField(default=False)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflowinfos', to='landmatrix.Deal')),
                ('deal_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workflowinfos', to='landmatrix.DealVersion')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestorVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, help_text='The date and time this revision was created.', verbose_name='date created')),
                ('serialized_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_by', models.ForeignKey(blank=True, help_text='The user who created this revision.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='versions', to='landmatrix.Investor')),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvestorWorkflowInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draft_status_before', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('draft_status_after', models.IntegerField(blank=True, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Activation'), (4, 'Rejected'), (5, 'To Delete')], null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True, default='')),
                ('processed_by_receiver', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflowinfos', to='landmatrix.Investor')),
                ('investor_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workflowinfos', to='landmatrix.InvestorVersion')),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='revision',
            name='user',
        ),
        migrations.AlterField(
            model_name='country',
            name='high_income',
            field=models.BooleanField(default=False, help_text='Target countries are countries that are NOT high income', verbose_name='High income'),
        ),
        migrations.DeleteModel(
            name='InvestorVentureInvolvementVersion',
        ),
        migrations.DeleteModel(
            name='Revision',
        ),
        migrations.AddField(
            model_name='deal',
            name='current_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landmatrix.DealVersion'),
        ),
        migrations.AddField(
            model_name='investor',
            name='current_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landmatrix.InvestorVersion'),
        ),
    ]
