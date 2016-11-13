from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery


from grid.forms.deal_general_form import DealGeneralForm


class ImplementationStatusQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('implementation_status', 'sub.implementation_status'),
        ('deal_count',         'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',          "ROUND(SUM(a.deal_size))")
    ]
    SUBQUERY_FIELDS = [
        ('implementation_status',    "a.implementation_status")
    ]
    GROUP_BY = ['sub.implementation_status']
    ORDER_BY = ['sub.implementation_status']

    IMPLEMENTATION_STATUS = list(filter(None, [c[0] and str(c[1]) or None for c in DealGeneralForm().fields["implementation_status"].choices]))

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