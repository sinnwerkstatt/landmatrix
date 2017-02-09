from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


from django.template.defaultfilters import slugify


class TransnationalDealsQuerySet(FakeQuerySetFlat):

    LONG_COUNTRIES = {
        'United States of America' : 'Usa*',
        'United Kingdom of Great Britain and Northern Ireland' : 'Uk*',
        'China, Hong Kong Special Administrative Region' : 'China, Hong Kong*',
        'China, Macao Special Administrative Region': 'China, Macao*',
        'Lao People\'s Democratic Republic' : 'Laos*',
        'United Republic of Tanzania' : 'Tanzania*',
        'Democratic Republic of the Congo' : 'DRC*',
        'Bolivia (Plurinational State of)' : 'Bolivia*',
        'The Former Yugoslav Republic of Macedonia': 'Macedonia*',
        'Venezuela (Bolivarian Republic of)': 'Venezuela*',
        'Republic of Moldova': 'Moldova*',
        'United Arab Emirates': 'Arab Emirates*',
        'Solomon Islands': 'Solomon Iss*',
        'Russian Federation': 'Russian Fed*',
        'Dominican Republic': 'Dominican Rep*',
        'Papua New Guinea': 'Papua New*',
        'Democratic People\'s Republic of Korea': 'North Korea*',
        'United States Virgin Islands': 'Virgin Iss*',
        'Iran (Islamic Republic of)': 'Iran*',
        'Syrian Arab Republic': 'Syria*',
        'Republic of Korea': 'South Korea*',
        'C\xf4te d\'Ivoire': 'Cote d\'Ivoire',
        'British Virgin Islands': 'British Virgin Iss*',
    }

    FIELDS = [
        ('target_country',   "CONCAT(deal_country.fk_region_id, '.', deal_country.name, '#!#', deal_country.id)"),
        ('investor_country', "ARRAY_AGG(DISTINCT CONCAT(investor_country.fk_region_id, '.', investor_country.name,  '#!#', investor_country.id))"),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
        "LEFT JOIN landmatrix_activityattribute         AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]
    ADDITIONAL_WHERES = ["investor_country.id <> deal_country.id"]
    GROUP_BY = ['target_country']

    def __init__(self, request):
        super().__init__(request)
        self.regions = request.GET.getlist("region", [])

    def shorten_country(self, country):
        country_parts = country.split(".")
        country_region = country_parts[0]
        if country_region in self.regions:
            country_region = -1
        return "%s.%s" % (country_region, self.LONG_COUNTRIES.get(country_parts[1], country_parts[1]))

    def all(self):
        from collections import OrderedDict

        region_sql = "AND deal_region.id in (%s) " % ", ".join(self.regions) if self.regions else ''
        self._filter_sql += region_sql

        t_deals = super().all()

        my_countries = {}
        for d in t_deals:
            target_country = d['target_country']
            country = self.country_dict(target_country, [self.shorten_country(dcountry.split("#!#")[0]) for dcountry in d['investor_country']])
            my_countries[self.shorten_country(target_country.split("#!#")[0])] = OrderedDict(sorted(country.items()))
            for investor_country in d['investor_country']:
                if investor_country.split("#!#")[0] not in my_countries:
                    country = self.country_dict(investor_country, [])
                    my_countries[self.shorten_country(investor_country.split("#!#")[0])] = OrderedDict(sorted(country.items()))

        my_countries = OrderedDict(sorted(my_countries.items(), key=lambda t: t[1]['id']))

        return list(my_countries.values())

    def country_dict(self, my_target_country, imports):
        country = {
            'name': self.shorten_country(my_target_country.split("#!#")[0]),
            'id': my_target_country.split("#!#")[1],
            'slug': slugify(my_target_country.split("#!#")[0].split(".")[1]),
            'size': 1,
            'imports': imports
        }
        return country


def original_sorting_order(index):
    order = { 'imports': 1, 'slug': 2, 'name': 3, 'size': 4, 'id': 5}
    return order[index]
