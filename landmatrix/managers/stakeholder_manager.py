from django.db import transaction
from django.db.models import Manager

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


@transaction.commit_manually
def flush_transaction():
    """
    Flush the current transaction so we don't read stale data

    Use in long running processes to make sure fresh data is read from
    the database.  This is a problem with MySQL and the default
    transaction mode.  You can fix it by setting
    "transaction-isolation = READ-COMMITTED" in my.cnf or by calling
    this function at the appropriate moment
    """
    transaction.commit()


class StakeholderManager(Manager):

    def raw_choices(self):
        flush_transaction()
        return self.raw("""
SELECT
  a.id,
  a.country,
  CONCAT(a.name, ' (', COALESCE(a.country, '-'), ', ', COALESCE(a.classification, '-'), ')') as name
FROM (
  SELECT
    s.id as id,
    (
      SELECT sag.attributes->'investor_name' AS aid
      FROM landmatrix_stakeholderattributegroup AS sag
      WHERE sag.fk_stakeholder_id = s.id AND sag.attributes ? 'investor_name'
      GROUP BY sag.attributes->'investor_name'
    ) AS name,
    (
      SELECT c.name AS aid
      FROM landmatrix_stakeholderattributegroup AS sag
      JOIN landmatrix_country AS c ON c.id = CAST(sag.attributes->'country' AS NUMERIC)
      WHERE sag.fk_stakeholder_id = s.id AND sag.attributes ? 'country'
      GROUP BY c.name
    ) AS country,
    (
      SELECT sag.attributes->'classification' AS aid
      FROM landmatrix_stakeholderattributegroup AS sag
      WHERE sag.fk_stakeholder_id = s.id AND sag.attributes ? 'classification'
      GROUP BY sag.attributes->'classification'
    ) AS classification
  FROM landmatrix_stakeholder AS s
  WHERE
    s.version = (
      SELECT max(version)
      FROM landmatrix_stakeholder smax, landmatrix_status st
      WHERE smax.fk_status_id = st.id AND smax.stakeholder_identifier = s.stakeholder_identifier AND st.name IN ('active', 'overwritten')
    )
    AND s.fk_status_id IS NOT NULL
  ORDER BY name
) as a;
""")
