from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.core.urlresolvers import reverse
from itertools import groupby

class TargetCountrySummariesQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('country_id', 'sub.country_id'),
        ('country',    'sub.country'),
        ('region',     'sub.name'),
        ('lat',        'sub.point_lat'),
        ('lon',        'sub.point_lon'),
        ('lat_min',    'sub.point_lat_min'),
        ('lon_min',    'sub.point_lon_min'),
        ('lat_max',    'sub.point_lat_max'),
        ('lon_max',    'sub.point_lon_max'),
        ('deals',      'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',   "ROUND(SUM(a.deal_size))"),
        ('intentions', 'ARRAY_AGG(sub.intention)')
    ]
    SUBQUERY_FIELDS = [
        ('country_id', "deal_country.id"),
        ('country', "deal_country.name"),
        ('name', "deal_region.name"),
        ('point_lat', "deal_country.point_lat"),
        ('point_lon', "deal_country.point_lon"),
        ('point_lat_min', "deal_country.point_lat_min"),
        ('point_lon_min', "deal_country.point_lon_min"),
        ('point_lat_max', "deal_country.point_lat_max"),
        ('point_lon_max', "deal_country.point_lon_max"),
        ('intention', "STRING_AGG(DISTINCT intention.value', ',')"),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id",
    ]
    ADDITIONAL_SUBQUERY_OPTIONS = "GROUP BY a.id, deal_country.id, deal_region.name"
    GROUP_BY = [
        'sub.country, sub.country_id, sub.name, '
        'sub.point_lat, sub.point_lon, '
        'sub.point_lat_min, sub.point_lon_min, sub.point_lat_max, sub.point_lon_max'
    ]

    def __init__(self, request):
        super().__init__(request)
        self.country_code = request.GET.get("country_code", None)
        self.region = request.GET.get("regions", None)

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
        c["country_url"] = reverse("table_list", kwargs={"group": "by-target-country", "group_value": c['country'].lower().replace(" ", "-")})

        filtered_intentions = [i for i in c['intentions'] if i]
        sorted_intentions = [self.map_intention(c) for c in sorted(filtered_intentions)]
        c["intentions"] = [
            "%s (%s)" % (key, len(list(group)))
            for key, group in groupby(sorted_intentions)
        ]
        return c

    def map_intention(self, intention):
        return intention.split(',')[0] if intention else None
