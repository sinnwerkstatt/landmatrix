from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.core.urlresolvers import reverse
from itertools import groupby

class TargetCountrySummariesQuerySet(FakeQuerySetWithSubquery):

    fields = [
        ('country_id', 'sub.country_id'),
        ('country',    'sub.country'),
        ('region',     'sub.name'),
        ('lat',        'sub.point_lat'),
        ('lon',        'sub.point_lon'),
        ('deals',      'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',   "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))"),
        ('intentions', 'ARRAY_AGG(sub.intention)')
    ]
    _subquery_fields = [
        ('country_id', "deal_country.id"),
        ('country', "deal_country.name"),
        ('name', "deal_region.name"),
        ('point_lat', "deal_country.point_lat"),
        ('point_lon', "deal_country.point_lon"),
        ('intention', "STRING_AGG(DISTINCT intention.attributes->'intention', ',')"),
    ]
    _additional_joins = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'",
        "LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'",
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id",
    ]
    _additional_subquery_options = "GROUP BY a.id, deal_country.id, deal_region.name"
    _group_by = ['sub.country, sub.country_id, sub.name, sub.point_lat, sub.point_lon']

    def __init__(self, get_data):
        super().__init__(get_data)
        self.country_code = get_data.get("country_code", None)
        self.region = get_data.get("regions", None)

    def all(self):
        if self.region:
            self._filter_sql += "AND deal_region.id = %s " % self.region
        if self.country_code:
            self._filter_sql += "AND deal_country.code_alpha3 = '%s' " % self.country_code

        countries_summary = super().all()
        return [self.to_json_record(c) for c in countries_summary if c['country_id']]

    def to_json_record(self, c):
        c['name'] = c['country']
        c["country_slug"] =c['country'].lower().replace(" ", "-")
        c["region_slug"] =c['region'].lower().replace(" ", "-")
        c["country_url"] = reverse("table_list", kwargs={"group": "by-target-country", "list": c['country'].lower().replace(" ", "-")})

        filtered_intentions = [i for i in c['intentions'] if i]
        sorted_intentions = [self.map_intention(c) for c in sorted(filtered_intentions)]
        c["intentions"] = [
            "%s (%s)" % (key, len(list(group)))
            for key, group in groupby(sorted_intentions)
        ]
        return c

    def map_intention(self, intention):
        return intention.split(',')[0] if intention else None
