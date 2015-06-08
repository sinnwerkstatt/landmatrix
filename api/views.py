__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *
from rest_framework import viewsets
from api.serializers import InvolvementSerializer
from django.db import models
from django.db import connection

class InvolvementViewSet(viewsets.ModelViewSet):
    queryset = Involvement.objects.all()
    serializer_class = InvolvementSerializer

class StatisticsManager(models.Manager):

    BASE_JOIN = """
        LEFT JOIN
          """ + Status.objects.model._meta.db_table + """ AS status
        ON (status.id = a.fk_status_id)
        LEFT JOIN
            """ + Involvement.objects.model._meta.db_table + """ AS i
        ON (i.fk_activity_id = a.id)
        LEFT JOIN
            """ + Stakeholder.objects.model._meta.db_table + """ AS s
        ON (i.fk_stakeholder_id = s.id)
        LEFT JOIN
            """ + PrimaryInvestor.objects.model._meta.db_table + """ AS pi
        ON (i.fk_primary_investor_id = pi.id)
        LEFT JOIN
            """ + Status.objects.model._meta.db_table + """ AS pi_st
        ON (pi.fk_status_id = pi_st.id)
        LEFT JOIN
          """ + StakeholderAttributeGroup.objects.model._meta.db_table + """ AS stakeholder_attrs
        ON (s.id = stakeholder_attrs.fk_stakeholder_id)
        LEFT JOIN
            """ + ActivityAttributeGroup.objects.model._meta.db_table + """ AS activity_attrs
        ON (a.id = activity_attrs.fk_activity_id)
        LEFT JOIN
          """ + Country.objects.model._meta.db_table + """ AS investor_country
        ON (stakeholder_attrs.attributes->'country' = investor_country.name)
        LEFT JOIN
          """ + Region.objects.model._meta.db_table + """ AS investor_region
        ON (investor_country.fk_region_id = investor_region.id)
        LEFT JOIN
             """ + Country.objects.model._meta.db_table + """ AS deal_country
        ON (activity_attrs.attributes->'target_country' = deal_country.name)
        LEFT JOIN
             """ + Region.objects.model._meta.db_table + """ AS deal_region
        ON (deal_country.fk_region_id = deal_region.id)
    """
    HECTARES_SQL = """
        ROUND(COALESCE(SUM(CAST(REPLACE(activity_attrs.attributes->'pi_deal_size', ',', '.') AS numeric)), 0)) AS deal_size
    """
    BASE_CONDITON = """
        a.version = (
            SELECT MAX(version)
            FROM
            """ + Activity.objects.model._meta.db_table + """ AS amax,
            """ + Status.objects.model._meta.db_table + """ AS st
            WHERE amax.fk_status_id = st.id
            AND amax.activity_identifier = a.activity_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
        )
        AND status.name IN ('active', 'overwritten')
        AND pi.version = (
            SELECT MAX(version)
            FROM """ + PrimaryInvestor.objects.model._meta.db_table + """ AS pimax,
            """ + Status.objects.model._meta.db_table + """ AS st
            WHERE pimax.fk_status_id = st.id
            AND pimax.primary_investor_identifier = pi.primary_investor_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
        )
        AND pi_st.name IN ('active', 'overwritten')
        AND activity_attrs.attributes->'pi_deal' = 'True'
    """

    def all(self):
        filter_sql = ''
        where_sql = ''
        cursor = connection.cursor()
        sql = """
            SELECT
                sub.negotiation_status,
                COUNT(DISTINCT a.activity_identifier) AS deals,
                """ + self.HECTARES_SQL + """,
                MIN(sub.negotiation_status_date) AS year
             FROM
                """ + Activity.objects.model._meta.db_table + """ AS a
             LEFT JOIN """ + ActivityAttributeGroup.objects.model._meta.db_table + """ AS activity_attrs
               ON a.id = activity_attrs.fk_activity_id,
                (SELECT DISTINCT
                   a.id,
                   activity_attrs.attributes->'pi_negotiation_status' AS negotiation_status,
                   activity_attrs.date AS negotiation_status_date
                 FROM
                   """ + Activity.objects.model._meta.db_table + """ AS a
                   """ + self.BASE_JOIN + """
                 WHERE
                   """ + self.BASE_CONDITON + """
                   """ + where_sql + """
                   """ + filter_sql + """) AS sub
             WHERE a.id = sub.id
             GROUP BY sub.negotiation_status
        """
        return cursor.execute(sql)
        result = cursor.fetchall()
        return list(result)

        pass

class StatisticsViewSet(viewsets.ModelViewSet):
    mgr = StatisticsManager()
    queryset = mgr.all()
#    pass