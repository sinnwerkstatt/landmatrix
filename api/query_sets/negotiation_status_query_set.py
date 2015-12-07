from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class NegotiationStatusQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('name', 'sub.negotiation_status'),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',          "ROUND(SUM(pi.deal_size))")
    ]
    SUBQUERY_FIELDS = [
        # ('negotiation_status', "negotiation.attributes->'pi_negotiation_status'"),
        # ('implementation_status', "implementation.attributes->'pi_implementation_status'")
        ('negotiation_status', 'pi.negotiation_status'),
        ('implementation_status', 'pi.implementation_status')
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'",
        "LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'",
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    ORDER_BY = ['sub.negotiation_status']
    GROUP_BY = ['sub.negotiation_status']
