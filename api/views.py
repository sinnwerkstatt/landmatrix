__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *
from rest_framework import viewsets
#from rest_framework import serializers
from api.serializers import *
from django.db import models
from django.db import connection

class InvolvementViewSet(viewsets.ModelViewSet):
    queryset = Involvement.objects.all()
    serializer_class = InvolvementSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer

class PrimaryInvestorViewSet(viewsets.ModelViewSet):
    queryset = PrimaryInvestor.objects.all()
    serializer_class = PrimaryInvestorSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ActivityAttributeGroupViewSet(viewsets.ModelViewSet):
    queryset = ActivityAttributeGroup.objects.all()
    serializer_class = ActivityAttributeGroupSerializer

class StatisticsManager(models.Manager):

    def all(self):
        BASE_JOIN = """
            LEFT JOIN
              """ + Status.objects.model._meta.db_table + """ AS status
            ON status.id = a.fk_status_id
            LEFT JOIN
                """ + Involvement.objects.model._meta.db_table + """ AS i
            ON i.fk_activity_id = a.id
            LEFT JOIN
                """ + Stakeholder.objects.model._meta.db_table + """ AS s
            ON i.fk_stakeholder_id = s.id
            LEFT JOIN
                """ + PrimaryInvestor.objects.model._meta.db_table + """ AS pi
            ON i.fk_primary_investor_id = pi.id
            LEFT JOIN
                """ + Status.objects.model._meta.db_table + """ AS pi_st
            ON pi.fk_status_id = pi_st.id
            LEFT JOIN
              """ + StakeholderAttributeGroup.objects.model._meta.db_table + """ AS stakeholder_attrs
            ON s.id = stakeholder_attrs.fk_stakeholder_id
            LEFT JOIN
                """ + ActivityAttributeGroup.objects.model._meta.db_table + """ AS activity_attrs
            ON a.id = activity_attrs.fk_activity_id
            LEFT JOIN
              """ + Country.objects.model._meta.db_table + """ AS investor_country
            ON stakeholder_attrs.attributes->'country' = investor_country.name
            LEFT JOIN
              """ + Region.objects.model._meta.db_table + """ AS investor_region
            ON investor_country.fk_region_id = investor_region.id
            LEFT JOIN
                 """ + Country.objects.model._meta.db_table + """ AS deal_country
            ON activity_attrs.attributes->'target_country' = deal_country.name
            LEFT JOIN
                 """ + Region.objects.model._meta.db_table + """ AS deal_region
            ON deal_country.fk_region_id = deal_region.id
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
        filter_sql = ''
        where_sql = ''
        cursor = connection.cursor()
        sql = """
            SELECT
                sub.negotiation_status,
                COUNT(DISTINCT a.activity_identifier) AS deals,
                """ + HECTARES_SQL + """,
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
                   """ + BASE_JOIN + """
                 WHERE
                   """ + BASE_CONDITON + """
                   """ + where_sql + """
                   """ + filter_sql + """) AS sub
             WHERE a.id = sub.id
             GROUP BY sub.negotiation_status
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        if connection.queries: print(connection.queries[-1]['sql'])
        return result

class StatisticsSerializer(serializers.Serializer):

    # should be of class serializer? hmm.
    data = list(StatisticsManager().all())

class StatisticsViewSet(viewsets.ModelViewSet):

    serializer_class = StatisticsSerializer

    def get_queryset(self):
        mgr = StatisticsManager()
        return mgr.all()

def stats():
    return 'woo hoo!'