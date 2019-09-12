#!/usr/bin/env python
import os
import sys
import csv
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections

from apps.landmatrix.models import Activity, ActivityAttribute


class Command(BaseCommand):
    help = 'Show all primary investors in old database that are assigned to deals in different target countries'

    def handle(self, *args, **options):
        self.stdout.write('Primary investor ID;Primary investor name;Deal IDs;Target Countries')
        for row in self.get_activities():
            self.stdout.write('%s;%s;%s;%s' % (
                row[0],
                row[1],
                row[2],
                row[3]
            ))

    def get_activities(self):
        sql = """
SELECT
  pi.primary_investor_identifier,
  pi.name,
  (SELECT GROUP_CONCAT(DISTINCT CONCAT('#', a.activity_identifier)) FROM involvements i LEFT JOIN activities a ON i.fk_activity = a.id WHERE i.fk_primary_investor = pi.id AND a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted")) GROUP BY pi.primary_investor_identifier) as `deal_ids`,
  (SELECT GROUP_CONCAT(DISTINCT v.value) FROM involvements i LEFT JOIN activities a ON i.fk_activity = a.id LEFT JOIN a_tag_groups tg ON i.fk_activity = tg.fk_activity LEFT JOIN a_tags t ON t.fk_a_tag_group = tg.id LEFT JOIN a_keys k ON k.id = t.fk_a_key LEFT JOIN a_values v ON v.id = t.fk_a_value WHERE i.fk_primary_investor = pi.id AND k.key = 'target_country' AND a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted")) GROUP BY pi.primary_investor_identifier) as `target_countries`
FROM primary_investors pi
WHERE pi.id in (SELECT pi2.id FROM primary_investors pi2 LEFT JOIN involvements i ON i.fk_primary_investor = pi2.id LEFT JOIN activities a on i.fk_activity = a.id WHERE a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted")))
AND pi.version = (.SELECT max(version) FROM primary_investors pi3 WHERE pi3.primary_investor_identifier = pi.primary_investor_identifier)
AND (SELECT COUNT(DISTINCT v.value) FROM involvements i LEFT JOIN activities a ON i.fk_activity = a.id LEFT JOIN a_tag_groups tg ON i.fk_activity = tg.fk_activity LEFT JOIN a_tags t ON t.fk_a_tag_group = tg.id LEFT JOIN a_keys k ON k.id = t.fk_a_key LEFT JOIN a_values v ON v.id = t.fk_a_value WHERE i.fk_primary_investor = pi.id AND k.key = 'target_country' AND a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted")) GROUP BY pi.primary_investor_identifier) > 1;
        """
        cursor = connections['v1_my'].cursor()
        cursor.execute(sql)
        return cursor.fetchall()
