from django.db import connection

from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery, FakeQuerySetFlat
from landmatrix.models.activity import Activity
from grid.views.filter_widget_mixin import FilterWidgetMixin


class StatisticsQuerySet(FakeQuerySetWithSubquery):

    DEBUG = False

    FIELDS = [
        ('negotiation_status',  'sub.negotiation_status'),
        ('deals',               'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',           "COALESCE(ROUND(SUM(a.deal_size)), 0)")
    ]
    SUBQUERY_FIELDS = [
        ('negotiation_status',    "a.negotiation_status")
    ]
    GROUP_BY = ['sub.negotiation_status']
    ORDER_BY = ['sub.negotiation_status']

    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]

    def __init__(self, request):
        self.disable_filters = request.GET.get('disable_filters', False)
        if self.disable_filters:
            # Backup
            request.session['disabled_filters'] = request.session.get('filters')
            request.session['disabled_set_default_filters'] = request.session.get(
                'set_default_filters', None)

            request.session['filters'] = {}
            if 'set_default_filters' in request.session:
                del(request.session['set_default_filters'])
            # TODO: This is ugly, move set_default_filters to somewhere else
            f = FilterWidgetMixin()
            f.request = request
            f.set_country_region_filter(request.GET.copy())
            f.set_default_filters(None, disabled_presets=[2,])
        super().__init__(request)
        self.country = request.GET.get('country')
        self.region = request.GET.get('region')
        self.request = request

    def all(self):
        self._filter_sql += self.regional_condition()
        output = [[r['negotiation_status'], r['deals'], r['deal_size']] for r in super().all()]
        if self.disable_filters:
            # restore original filters
            self.request.session['filters'] = self.request.session.get('disabled_filters')
            if self.request.session['disabled_set_default_filters'] is not None:
                self.request.session['set_default_filters'] = self.request.session[
                    'disabled_set_default_filters']
            del(self.request.session['disabled_filters'])
            del(self.request.session['disabled_set_default_filters'])
        #raise IOError(self.sql_query())
        return output

    def regional_condition(self):
        if self.country:
            return "AND deal_country.id = %s" % self.country
        elif self.region:
            return "AND deal_country.fk_region_id = %s" % self.region
        return ''

    def is_public_condition(self):
        return "a.is_public = 't'"


class PublicDealCountQuerySet(FakeQuerySetFlat):

    DEBUG = False

    def all(self):
        cursor = connection.cursor()
        sql = """
    SELECT
        COUNT(DISTINCT a.activity_identifier) AS deals
    FROM """ + Activity._meta.db_table + """ AS a
    WHERE
        """ + "\nAND ".join(filter(None, [
                self.status_active_condition(),
                self.is_public_condition(),
            ]))

        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def is_public_condition(self):
        return "a.is_public = 't'"
    