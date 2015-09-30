from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class HectaresQuerySet(FakeQuerySetWithSubquery):

    fields = [
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]
    _subquery_fields = []
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]

    def all(self):
        data = super().all()
        return data[0] if data else {}
