__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .sql_builder import SQLBuilder, join_attributes

class SubqueryBuilder(SQLBuilder):


    @classmethod
    def get_base_sql(cls):
        return u"""SELECT DISTINCT
            a.id AS id,
            %(name)s AS name,
%(columns)s              'dummy' AS dummy
          FROM
              landmatrix_activity AS a
              JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
%(from)s""" + "\n" \
                  + join_attributes('pi_deal') + "\n" \
                  + join_attributes('deal_scope') + """
%(from_filter)s
          WHERE
              a.version = (
                  SELECT max(version)
                  FROM landmatrix_activity amax, landmatrix_status st
                  WHERE amax.fk_status_id = st.id
                      AND amax.activity_identifier = a.activity_identifier
                      AND st.name IN ('active', 'overwritten', 'deleted')
              )
              AND landmatrix_status.name IN ('active', 'overwritten')
              AND pi_deal.attributes->'pi_deal' = 'True'
              AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
              %(where)s
              %(where_filter)s
          GROUP BY a.id
    """
