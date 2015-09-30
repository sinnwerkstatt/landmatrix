from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.add_deal_general_form import AddDealGeneralForm


class ImplementationStatusQuerySet(FakeQuerySetWithSubquery):

    fields = [
        ('implementation_status', 'sub.implementation_status'),
        ('deal_count',         'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]
    _subquery_fields = [
        ('negotiation_status', "negotiation.attributes->'pi_negotiation_status'"),
        ('implementation_status',    "implementation.attributes->'pi_implementation_status'")
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    GROUP_BY = ['sub.implementation_status']
    ORDER_BY = ['sub.implementation_status']

    IMPLEMENTATION_STATUS = list(filter(None, [c[0] and str(c[1]) or None for c in AddDealGeneralForm().fields["implementation_status"].choices]))

    def all(self):
        found = super().all()
        output = []
        stati = {}

        for i in found:
            name = i.get('implementation_status', '')
            stati[name] = {
                "name": name,
                "deals": i['deal_count'],
                "hectares": i['deal_size'],
            }
        for i in self.IMPLEMENTATION_STATUS:
            output.append(stati.get(i, {"name": i, "deals": 0, "hectares": 0}))
        output.append(stati.get("", {"name": "", "deals": 0, "hectares": 0}))

        return output