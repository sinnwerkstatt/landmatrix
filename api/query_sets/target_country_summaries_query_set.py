from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


from django.core.urlresolvers import reverse
from itertools import groupby

class TargetCountrySummariesQuerySet(FakeQuerySetFlat):

    FIELDS = [
        ('country_id',   "deal_country.id"),
        ('country',      "deal_country.name"),
        ('country_slug', 'deal_country.slug'),
        ('region',       'deal_region.name'),
        ('region_slug',  'deal_region.slug'),
        ('lat',          "deal_country.point_lat"),
        ('lon',          "deal_country.point_lon"),
        ('lat_min',      "deal_country.point_lat_min"),
        ('lon_min',      "deal_country.point_lon_min"),
        ('lat_max',      "deal_country.point_lat_max"),
        ('lon_max',      "deal_country.point_lon_max"),
        ('deals',        'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',     "ROUND(SUM(a.deal_size))"),
        ('domestic',     'COUNT(DISTINCT CASE WHEN investor_country.id = deal_country.id THEN a.activity_identifier ELSE NULL END)'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id",
        "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
        "LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id",
    ]
    #ADDITIONAL_SUBQUERY_OPTIONS = "GROUP BY a.id, deal_country.id, deal_region.name"
    GROUP_BY = [
        'deal_country.id',
        'deal_country.name',
        'deal_country.slug',
        'deal_region.name',
        'deal_region.slug',
        'deal_country.point_lat',
        'deal_country.point_lon',
        'deal_country.point_lat_min',
        'deal_country.point_lon_min',
        'deal_country.point_lat_max',
        'deal_country.point_lon_max',
    ]

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get("target_country", None)
        self.region = request.GET.get("target_region", None)

    #def all(self):
    #    if self.region:
    #        self._filter_sql += "AND deal_region.id = %s " % self.region
    #    if self.country_code:
    #        self._filter_sql += "AND deal_country.code_alpha3 = '%s' " % self.country_code
    #    countries_summary = super().all()
    #    return [self.to_json_record(c) for c in countries_summary if c['country_id']]

    def all(self):
        if self.region:
            try:
                region = int(self.region)
            except ValueError:
                pass
            else:
                self._filter_sql += "AND deal_region.id = %s " % region
        if self.country:
            try:
                country = int(self.country)
            except ValueError:
                pass
            else:
                self._filter_sql += "AND deal_country.id = %s " % country

        countries_summary = super().all()

        countries = {}
        for c in countries_summary:
            if not c['country_id']: continue
            country = countries.get(c['country_id'], {"domestic": 0, "transnational": 0})
            country.update(self.to_json_record(c, country))
            countries.update({c['country_id']: country})

        return [v for k,v in countries.items()]

    def to_json_record(self, c, country):
        c['name'] = c['country']
        c["country_slug"] = c['country_slug']
        c["region_slug"] = c['region_slug']
        c['url'] = reverse("table_list", kwargs={"group": "by-target-country", "group_value": c['country'].lower().replace(" ", "-")})
        c['transnational'] = c['deals'] - c['domestic']
        c['deals'] = c['deals'] + country.get("deals", 0)

        return c

    #def to_json_record(self, c):
    #    c['name'] = c['country']
    #    c["country_slug"] =c['country'].lower().replace(" ", "-")
    #    c["region_slug"] =c['region'].lower().replace(" ", "-")
    #    c["country_url"] = reverse("table_list", kwargs={"group": "by-target-country", "group_value": c['country'].lower().replace(" ", "-")})
#
    #    filtered_intentions = [i for i in c['intentions'] if i]
    #    sorted_intentions = [self.map_intention(c) for c in sorted(filtered_intentions)]
    #    c["intentions"] = [
    #        "%s (%s)" % (key, len(list(group)))
    #        for key, group in groupby(sorted_intentions)
    #    ]
    #    return c
#
    #def map_intention(self, intention):
    #    return intention.split(',')[0] if intention else None
