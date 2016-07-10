from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat
import timeit

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealsQuerySet(FakeQuerySetFlat):

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    FIELDS = [
        (   'deal_id',
            'a.activity_identifier'
        ),
        (
            'point_lat',
            "point_lat.value"
        ),
        (
            'point_lon',
            "point_lon.value"
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
            'intended_area.polygon',
        ),
        (
            'production_area',
            'production_area.polygon',
        ),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute    AS point_lat        ON a.id = point_lat.fk_activity_id AND point_lat.name = 'point_lat'",        
        "LEFT JOIN landmatrix_activityattribute    AS point_lon        ON a.id = point_lon.fk_activity_id AND point_lon.name = 'point_lon'",
        "LEFT JOIN landmatrix_activityattribute    AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'",
        "LEFT JOIN landmatrix_activityattribute    AS intended_size    ON a.id = intended_size.fk_activity_id AND intended_size.name = 'intended_size'",
        "LEFT JOIN landmatrix_activityattribute    AS contract_size    ON a.id = contract_size.fk_activity_id AND contract_size.name = 'contract_size'",
        "LEFT JOIN landmatrix_activityattribute    AS production_size  ON a.id = production_size.fk_activity_id AND production_size.name = 'production_size'",
        "LEFT JOIN landmatrix_activityattribute    AS intended_area    ON a.id = intended_area.fk_activity_id AND intended_area.name = 'intended_area' AND ST_IsValid(intended_area.polygon)"
        "LEFT JOIN landmatrix_activityattribute    AS production_area    ON a.id = production_area.fk_activity_id AND production_area.name = 'production_area' AND ST_IsValid(production_area.polygon)"
    ]
    ADDITIONAL_WHERES = [
        "point_lat.name = 'point_lat' AND point_lon.name = 'point_lon'",
    ]
    GROUP_BY = [
        'point_lat.value', 'point_lon.value', 'intended_area.polygon',
        'production_area.polygon', 'intended_size.value',
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
        if request.GET.get('window'):
            lat_min, lat_max, lon_min, lon_max = request.GET.get('window').split(',')
            self._set_window(lat_min, lat_max, lon_min, lon_max)

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

    def _set_window(self, lat_min, lat_max, lon_min, lon_max):
        # respect the 180th meridian
        if lon_min > lon_max: lon_max, lon_min = lon_min, lon_max
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "CAST(point_lat.value AS NUMERIC) >= " + lat_min,
                "CAST(point_lat.value AS NUMERIC) <= " + lat_max,
                "CAST(point_lon.value AS NUMERIC) >= " + lon_min,
                "CAST(point_lon.value AS NUMERIC) <= " + lon_max,
        ])

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
