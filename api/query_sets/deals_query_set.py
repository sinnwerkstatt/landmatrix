import timeit

from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealsQuerySet(FakeQuerySetFlat):
    FIELDS = [
        (   'deal_id',
            'a.activity_identifier'
        ),
        (
            'point_lat',
            "ARRAY_TO_STRING(ARRAY_AGG(location.point_lat ORDER BY location.group_name),';')"
        ),
        (
            'point_lon',
            "ARRAY_TO_STRING(ARRAY_AGG(location.point_lon ORDER BY location.group_name),';')"
        ),
        (
            'intention',
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intention.value), ', '), '')"
        ),
        (
            'intended_size',
            "intended_size.value"
        ),
         # "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.name = 'intended_size'), ', '), '')"),
        (
            'contract_size',
            "contract_size.value"
        ),
         # "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.name = 'contract_size'), ', '), '')"),
        (
            'production_size',
            "production_size.value"
        ),
         # "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT production_size.name = 'production_size'), ', '), '')"),
        (
            'investor',
            'operational_stakeholder.name'
        ),
        (
            'intended_area',
            "ARRAY_TO_STRING(ARRAY_AGG(location.intended_area ORDER BY location.group_name),';')",
        ),
        (
            'production_area',
            "ARRAY_TO_STRING(ARRAY_AGG(location.production_area ORDER BY location.group_name),';')",
        ),
    ]
    # Location subquery is sadly required to avoid crossing lats/longs between
    # multiple locations
    LOCATION_JOIN = """
    LEFT JOIN (
        SELECT aag.name AS group_name,
            point_lat.fk_activity_id AS fk_activity_id,
            CAST(point_lat.value AS NUMERIC) AS point_lat,
            CAST(point_lon.value AS NUMERIC) AS point_lon,
            intended_area.polygon AS intended_area,
            production_area.polygon AS production_area
        FROM landmatrix_activityattributegroup AS aag
        LEFT JOIN
            landmatrix_activityattribute AS point_lat
                ON (point_lat.name = 'point_lat'
                AND point_lat.fk_group_id = aag.id)
        LEFT JOIN landmatrix_activityattribute AS point_lon
                ON (point_lon.name = 'point_lon'
                AND point_lon.fk_group_id = aag.id
                AND point_lon.fk_activity_id = point_lat.fk_activity_id)
        LEFT JOIN landmatrix_activityattribute AS intended_area
                ON (intended_area.name = 'intended_area'
                AND intended_area.fk_group_id = aag.id
                AND intended_area.fk_activity_id = point_lat.fk_activity_id
                AND ST_IsValid(intended_area.polygon))
        LEFT JOIN landmatrix_activityattribute AS production_area
                ON (production_area.name = 'production_area'
                AND production_area.fk_group_id = aag.id
                AND production_area.fk_activity_id = point_lat.fk_activity_id
                AND ST_IsValid(production_area.polygon))
        WHERE aag.name LIKE 'location%%' AND
        %s
    ) location ON location.fk_activity_id = a.id
    """
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute    AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'",
        "LEFT JOIN landmatrix_activityattribute    AS intended_size    ON a.id = intended_size.fk_activity_id AND intended_size.name = 'intended_size'",
        "LEFT JOIN landmatrix_activityattribute    AS contract_size    ON a.id = contract_size.fk_activity_id AND contract_size.name = 'contract_size'",
        "LEFT JOIN landmatrix_activityattribute    AS production_size  ON a.id = production_size.fk_activity_id AND production_size.name = 'production_size'",
    ]
    ADDITIONAL_WHERES = []
    GROUP_BY = [
        'intended_size.value',
        'contract_size.value', 'production_size.value',
        'operational_stakeholder.name', 'a.activity_identifier'
    ]

    def __init__(self, request):
        if 'deal_scope' not in request.GET:
            request.GET = request.GET.copy()
            request.GET.setlist('deal_scope', ['domestic', 'transnational'])
        super().__init__(request)
        self._set_limit(request.GET.get('limit'))
        self._set_investor_country(request.GET.get('investor_country'))
        self._set_investor_region(request.GET.get('investor_region'))
        self._set_target_country(request.GET.get('target_country'))
        self._set_target_region(request.GET.get('target_region'))
        self._set_attributes(request.GET.getlist('attributes', []))

        window_set = False
        if request.GET.get('window'):
            lon_min, lat_min, lon_max, lat_max = request.GET.get('window').split(',')
            window_set = self._set_window(lat_min, lon_min, lat_max, lon_max)

        if not window_set:
            location_join = self.LOCATION_JOIN % ' TRUE'
            self._additional_joins = add_to_list_if_not_present(
                self._additional_joins, [location_join])

    def all(self):
        start_time = timeit.default_timer()
        output = super().all()

        if self.DEBUG:
            print('Query time:', timeit.default_timer() - start_time)

        return output

    def _set_attributes(self, attributes):
        # intention is already in the base joins and i can't be bothered to do it cleanly now, so:
        if 'intention' in attributes: attributes.remove('intention')

        for attribute in attributes:
            self._fields = add_to_list_if_not_present(
                self._fields, [(attribute, "%(name)s.name = '%(name)s'" % { 'name': attribute })]
            )
            self._additional_joins = add_to_list_if_not_present(
                self._additional_joins, [
                    "LEFT JOIN landmatrix_activityattribute    AS %(name)s  ON a.id = %(name)s.fk_activity_id AND %(name)s.name = '%(name)s'" % {
                    'name': attribute
                    }
                ])
            self._group_by = add_to_list_if_not_present(
                self._group_by, ['%s.name' % attribute]
            )

    def _set_limit(self, limit):
        if limit and ',' in limit:
            limit = '%s OFFSET %s' % (
                limit.split(',')[0],
                limit.split(',')[1]
            )
        self._limit = limit

    def _set_investor_country(self, country_id):
        if not country_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
                "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, ["stakeholder.fk_country_id = %s" % country_id]
        )

    def _set_investor_region(self, region_id):
        if not region_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
                "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
                "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, ["investor_country.fk_region_id = " + region_id]
        )

    def _set_target_country(self, country_id):
        if not country_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, ["target_country.value = '%s'" % country_id]
        )

    def _set_target_region(self, region_id):
        if not region_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
                "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id"
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, ["deal_country.fk_region_id = " + region_id]
        )

    def _set_window(self, lat_min, lon_min, lat_max, lon_max):
        try:
            lat_min, lat_max = float(lat_min), float(lat_max)
            lon_min, lon_max = float(lon_min), float(lon_max)
        except ValueError:
            # Don't set a window with bogus values
            return False

        # respect the 180th meridian
        if lon_min > lon_max:
            lon_max, lon_min = lon_min, lon_max
        if lat_min > lat_max:
            lat_max, lat_min = lat_min, lat_max

        window_join_wheres = [
            "CAST(point_lat.value AS NUMERIC) >= {}".format(lat_min),
            "CAST(point_lat.value AS NUMERIC) <= {}".format(lat_max),
            "CAST(point_lon.value AS NUMERIC) >= {}".format(lon_min),
            "CAST(point_lon.value AS NUMERIC) <= {}".format(lon_max),
        ]
        location_join = self.LOCATION_JOIN % ' AND '.join(window_join_wheres)
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [location_join])

        window_wheres = [
            "location.point_lat >= {}".format(lat_min),
            "location.point_lat <= {}".format(lat_max),
            "location.point_lon >= {}".format(lon_min),
            "location.point_lon <= {}".format(lon_max),
        ]
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, window_wheres)

        return True

    def _set_negotiation_status(self, negotiation_status):
        if not negotiation_status: return
        stati = []
        for n in negotiation_status:
            stati.extend(self.BASE_FILTER_MAP.get(n))

        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, ["LOWER(a.negotiation_status) IN ('%s') " % "', '".join(stati)]
        )


def add_to_list_if_not_present(old_list, additional_elements):
    for element in additional_elements:
        if not element in old_list:
            old_list = old_list + [element]
    return old_list
