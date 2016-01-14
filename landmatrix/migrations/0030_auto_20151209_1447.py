# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0029_auto_20151203_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='involvement',
            name='fk_activity',
        ),
        migrations.RemoveField(
            model_name='involvement',
            name='fk_primary_investor',
        ),
        migrations.RemoveField(
            model_name='involvement',
            name='fk_stakeholder',
        ),
        migrations.DeleteModel(
            name='Involvement',
        ),
        migrations.RemoveField(
            model_name='primaryinvestor',
            name='fk_status',
        ),
        migrations.DeleteModel(
            name='PrimaryInvestor',
        ),
        migrations.RemoveField(
            model_name='stakeholder',
            name='fk_status',
        ),
        migrations.RemoveField(
            model_name='stakeholderattributegroup',
            name='fk_language',
        ),
        migrations.RemoveField(
            model_name='stakeholderattributegroup',
            name='fk_stakeholder',
        ),
        migrations.DeleteModel(
            name='Stakeholder',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='fk_stakeholder_attribute_group',
        ),
        migrations.DeleteModel(
            name='StakeholderAttributeGroup',
        ),
    ]
