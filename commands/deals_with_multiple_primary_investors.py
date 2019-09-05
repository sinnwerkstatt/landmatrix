#!/usr/bin/env python
from django.core.management import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Show all deals in old database with multiple primary investors'

    def handle(self, *args, **options):
        self.stdout.write('Deal ID;Primary investor count;Primary investors')
        for row in self.get_activities():
            self.stdout.write('%s;%s;%s' % (
                row[0],
                row[1],
                row[2]
            ))

    def get_activities(self):
        sql = """
SELECT
  CONCAT('#', a.activity_identifier),
  (SELECT COUNT(DISTINCT pi.primary_investor_identifier) FROM involvements i LEFT JOIN primary_investors pi ON i.fk_primary_investor = pi.id WHERE i.fk_activity = a.id GROUP BY a.id) as `pi_count`,
  (SELECT GROUP_CONCAT(DISTINCT pi.primary_investor_identifier, ' (', pi.name, ')') FROM involvements i LEFT JOIN primary_investors pi ON i.fk_primary_investor = pi.id WHERE i.fk_activity = a.id GROUP BY a.id) as `pi`
FROM activities a
WHERE a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
AND (SELECT COUNT(DISTINCT pi.primary_investor_identifier) FROM involvements i LEFT JOIN primary_investors pi ON i.fk_primary_investor = pi.id WHERE i.fk_activity = a.id GROUP BY a.id)  > 1
GROUP BY a.activity_identifier;
        """
        cursor = connections['v1_my'].cursor()
        cursor.execute(sql)
        return cursor.fetchall()
