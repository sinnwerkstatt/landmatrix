from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class NegotiationStatusQuerySet(FakeQuerySetWithSubquery):

    fields = [
        ('name', 'sub.negotiation_status'),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]
    _subquery_fields = [
        ('negotiation_status', "negotiation.attributes->'pi_negotiation_status'"),
        ('implementation_status', "implementation.attributes->'pi_implementation_status'")
    ]
    _additional_joins = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'",
        "LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'",
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    _order_by = ['sub.negotiation_status']
    _group_by = ['sub.negotiation_status']
