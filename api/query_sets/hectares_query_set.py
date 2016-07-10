from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class HectaresQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',          "ROUND(SUM(a.deal_size))")
    ]
    SUBQUERY_FIELDS = []

    def all(self):
        data = super().all()
        return data[0] if data else {}
