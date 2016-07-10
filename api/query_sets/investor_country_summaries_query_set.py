from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat
from django.core.urlresolvers import reverse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorCountrySummariesQuerySet(FakeQuerySetFlat):

    FIELDS = [
        ('country_id',   'investor_country.id'),
        ('country',      'investor_country.name'),
        ('country_slug', 'investor_country.slug'),
        ('region',       'investor_region.name'),
        ('region_slug',  'investor_region.slug'),
        ('lat',          'investor_country.point_lat'),
        ('lon',          'investor_country.point_lon'),
        ('lat_min',      'investor_country.point_lat_min'),
        ('lon_min',      'investor_country.point_lon_min'),
        ('lat_max',      'investor_country.point_lat_max'),
        ('lon_max',      'investor_country.point_lon_max'),
        ('deals',        'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_scope',   "a.deal_scope")
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
        "LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]
    GROUP_BY = [
        "investor_country.id, investor_region.name, a.deal_scope",
        "investor_country.slug, investor_region.slug",
    ]

    def all(self):
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
        c[c['deal_scope']] = c['deals'] + country.get(c['deal_scope'], 0)
        c['deals'] = c['deals'] + country.get("deals", 0)

        return c
