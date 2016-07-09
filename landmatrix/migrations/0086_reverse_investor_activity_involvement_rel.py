# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

#def update_investor_activity_involvements(apps, schema_editor):
#    InvestorActivityInvolvement = apps.get_model("landmatrix", "InvestorActivityInvolvement")
#    Activity = apps.get_model("landmatrix", "Activity")
#    HistoricalActivity = apps.get_model("landmatrix", "HistoricalActivity")
#    for inv in InvestorActivityInvolvement.objects.all():
#        activity = Activity.objects.filter(activity_identifier=inv.fk_activity.activity_identifier).order_by('-id').first()
#        hactivity, created = HistoricalActivity.objects.get_or_create(id=activity.id, activity_identifier=activity.activity_identifier)
#        if inv.fk_activity_id != activity.id:
#            inv.fk_activity_id = activity.id
#            inv.save()

class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0085_switch_investor_activity_involvement_rel'),
    ]

    operations = [
        #migrations.RunPython(update_investor_activity_involvements),
        migrations.AlterField(
            model_name='investoractivityinvolvement',
            name='fk_activity',
            field=models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity'),
        ),
    ]
