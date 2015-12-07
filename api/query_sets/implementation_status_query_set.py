from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.add_deal_general_form import AddDealGeneralForm


class ImplementationStatusQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('implementation_status', 'sub.implementation_status'),
        ('deal_count',         'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',          "ROUND(SUM(pi.deal_size))")
    ]
    SUBQUERY_FIELDS = [
        ('negotiation_status', "pi.negotiation_status"),
        ('implementation_status',    "pi.implementation_status")
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