"""
Handle filtering of activities by various datapoints.

Filtering is pretty complex and extends into api, grid, charts, and map views.
We try to collect it here in api where possible....
"""
import json
import operator
from collections import OrderedDict

from django.http import QueryDict
from django.utils.translation import gettext_lazy as _

# We can't import from landmatrix.models as FilterCondition imports from here
from apps.landmatrix.models.activity import HistoricalActivity
from apps.landmatrix.models.country import Country

FILTER_FORMATS_SQL = 0
FILTER_FORMATS_ELASTICSEARCH = 1


# operation => (numeric operand, character operand, description )
# This is an ordered dict as the keys are used to generate model choices.
# It is here in order to resolve circular imports
FILTER_OPERATION_MAP = OrderedDict(
    [
        ("is", ("{column} = {value}", "{column} = '{value}'", _("is"))),
        ("in", ("{column} IN ({value})", "{column} IN ({value})", _("is one of"))),
        (
            "not_in",
            (
                "{column} NOT IN ({value})",
                "{column} NOT IN ({value})",
                _("isn't any of"),
            ),
        ),
        ("gte", ("{column} >= {value}", "{column} >= '{value}'", _("is >="))),
        ("gt", ("{column} > {value}", "{column} > '{value}'", _("is >"))),
        ("lte", ("{column} <= {value}", "{column} <= '{value}'", _("is <="))),
        ("lt", ("{column} < {value}", "{column} < '{value}'", _("is <"))),
        (
            "contains",
            (
                "{column} LIKE '%%%%%%%%{value}%%%%%%%%'",
                "{column} LIKE '%%%%%%%%{value}%%%%%%%%'",
                _("contains"),
            ),
        ),
        (
            "not_contains",
            (
                "{column} NOT LIKE '%%%%%%%%{value}%%%%%%%%'",
                "{column} NOT LIKE '%%%%%%%%{value}%%%%%%%%'",
                _("not contains"),
            ),
        ),
        ("is_empty", ("{column} IS NULL", "{column} IS NULL", _("is empty"))),
        (
            "excludes",
            (
                "NOT EXISTS (SELECT * from {table} where a.id = fk_activity_id AND name = '{variable}' "
                "AND {column} = {value})",
                "NOT EXISTS (SELECT * from {table} where a.id = fk_activity_id AND name = '{variable}' "
                "AND {column} = '{value}')",
                _("excludes"),
            ),
        ),
    ]
)


def get_elasticsearch_match_operation(operator, variable_name, value):
    """
    Returns an elasticsearch-conform Match phrase for each SQL-operator
    """
    if operator == "is":
        return ("must", {"match_phrase": {variable_name: value}})
    if operator == "in":
        return ("should", {"match_phrase": {variable_name: value}})
    if operator == "not_in":
        return ("must_not", {"match_phrase": {variable_name: value}})
    if operator == "gte":
        return ("must", {"range": {variable_name: {"gte": value}}})
    if operator == "gt":
        return ("must", {"range": {variable_name: {"gt": value}}})
    if operator == "lte":
        return ("must", {"range": {variable_name: {"lte": value}}})
    if operator == "lt":
        return ("must", {"range": {variable_name: {"lt": value}}})
    if operator == "contains":
        return (
            "must",
            {
                "bool": {
                    "should": [
                        {"match_phrase": {"name": value.lower()}},
                        {"wildcard": {variable_name: "*%s*" % value.lower()}},
                    ],
                    "minimum_should_match": 1,
                }
            },
        )
    if operator == "not_contains":
        return ("must_not", {"match": {variable_name: value}})
    if operator == "excludes":
        return ("must_not", {"match": {variable_name: value}})
    if operator == "is_empty":
        if "date" in variable_name:
            # Check for null values
            return (
                "must",
                {"bool": {"must_not": {"exists": {"field": variable_name}}}},
            )
        else:
            # Check for empty strings
            return ("must", {"match_phrase": {variable_name: ""}})


# TODO: this counter is shared by all users, and is per thread.
# It should probably be moved to the session
FILTER_COUNTER = 0


# TODO: convert to object, these don't need to be dicts.
class BaseFilter(dict):
    ACTIVITY_TYPE = "activity"
    INVESTOR_TYPE = "investor"

    @property
    def name(self):
        return self["name"]

    @property
    def type(self):
        if "operating_company_" in self["variable"]:
            return self.INVESTOR_TYPE
        elif "parent_stakeholder_" in self["variable"]:
            return self.INVESTOR_TYPE
        elif "parent_investor_" in self["variable"]:
            return self.INVESTOR_TYPE
        else:
            return self.ACTIVITY_TYPE


class Filter(BaseFilter):

    VARIABLE_MAPPING = {"operational_stakeholder": "operating_company_id"}

    def __init__(
        self,
        variable,
        operator,
        value,
        name=None,
        label=None,
        key=None,
        display_value=None,
    ):
        if operator not in FILTER_OPERATION_MAP:
            raise ValueError("No such operator: {}".format(operator))

        if not display_value:
            display_value = value

        variable = self.VARIABLE_MAPPING.get(variable, variable)

        super().__init__(
            name=name,
            variable=variable,
            operator=operator,
            value=value,
            label=label,
            key=key,
            display_value=display_value,
        )

    @classmethod
    def from_session(cls, filter_dict):
        """
        Because filters inherit from dict, they are stored in the session
        as dicts.
        """
        return cls(
            filter_dict["variable"],
            filter_dict["operator"],
            filter_dict["value"],
            name=filter_dict.get("name"),
            label=filter_dict.get("label"),
            key=filter_dict.get("key"),
            display_value=filter_dict.get("display_value"),
        )

    def to_sql_format(self):
        """
        Converts a filter into the format used by FilterToSql:
        {'variable__operator': value}
        """
        key = self["key"] or "value"
        # TODO: hopefully _parse_value is no longer required
        value = self.parse_value(self["value"], variable=self["variable"], key=key)

        if "in" in self["operator"] and not isinstance(value, list):
            value = [value]

        definition_key = "__".join((self["variable"], key, self["operator"]))
        formatted_filter = {definition_key: value}

        return formatted_filter

    def parse_value(self, filter_value, variable=None, key=None):
        """
        Necessary due to the different ways single values and lists are stored
        in DB and session.
        """
        if isinstance(filter_value, (list, tuple)):
            if len(filter_value) > 1:
                return filter_value
            if len(filter_value) > 0:
                value = filter_value[0]
            else:
                value = ""
        else:
            value = filter_value
        if "[" in value:
            value = [str(v) for v in json.loads(value)]

        if variable is not None and key is not None:
            # Is this still required? Why not just always store ids?
            is_country_string = (
                "country" in variable and key == "value" and not value.isnumeric()
            )
            if is_country_string:
                country = Country.objects.defer("geom").get(
                    name__iexact=value.replace("-", " ")
                )
                value = str(country.pk)

        return value

    def to_elasticsearch_match(self):
        """Will return an elasticsearch operator term and an elasticsearch-format Match or Bool
        (for multiple matches) dictionary object.
        Example: ('must', {'match': {'intention__value': 3},
                                     '_filter_name': 'intention__value__is'})
        Example2: ('must_not', {'bool':
                      {'should': [
                          {'match': {'intention__value': 3}},
                          {'match': {'intention__value': 3}}
                      ]},
                   '_filter_name': 'intention__value__not_in'
                  })
        Note: This comes with an added '_filter_name' attribute for internal aggregation
              which needs to be removed."""

        key = self["key"] or "value"
        value = self.parse_value(self["value"], variable=self["variable"], key=key)
        definition_key = "__".join((self["variable"], key, self["operator"]))

        # only the starting operator of this match or query-match is important for the logical operation,
        # we now map which one
        elastic_operator = None
        if "in" in self["operator"] and isinstance(value, list) and len(value) > 1:
            # generate multiple matches
            matches = []
            inside_operator = None
            for single_value in value:
                operator, partial_match = get_elasticsearch_match_operation(
                    self["operator"], self["variable"], single_value
                )
                inside_operator = operator
                matches.append(partial_match)
            match = {"bool": {inside_operator: matches}, "_filter_name": definition_key}
            if inside_operator == "should":
                match["bool"]["minimum_should_match"] = 1
            elastic_operator = "must"
            # 'must' is always right here, because the list makes the query already a composite, and the inner operator has effect
        else:
            if isinstance(value, list):
                if len(value) > 1:
                    print(
                        'WARNING: converting a filter without "in" with 2 or more values into a single match!'
                    )
                value = value[0]
            if self["operator"] == "in":
                self["operator"] = "is"
            # Boolean fields can be 'False' or not existing. Check for not 'True' instead.
            if self["operator"] == "is" and self["value"] == "False":
                self["operator"], value = "not_in", "True"
            # generate single value match
            elastic_operator, match = get_elasticsearch_match_operation(
                self["operator"], self["variable"], value
            )

            match.update({"_filter_name": definition_key})

        return (elastic_operator, match)


class PresetFilter(BaseFilter):
    def __init__(self, preset, name=None, label=None, hidden=False):
        from apps.landmatrix.models.filter import FilterPreset

        if isinstance(preset, FilterPreset):
            self.preset_id = preset.pk
            self.filter = preset
        else:
            self.preset_id = preset
            self.filter = FilterPreset.objects.get(id=self.preset_id)

        if label is None:
            label = self.filter.name

        super().__init__(
            name=name, preset_id=self.preset_id, label=label, hidden=hidden
        )

    @classmethod
    def from_session(cls, filter_dict):
        """
        Because filters inherit from dict, they are stored in the session
        as dicts.
        """
        return cls(
            filter_dict["preset_id"],
            name=filter_dict.get("name"),
            label=filter_dict.get("label"),
            hidden=filter_dict.get("hidden", False),
        )


def load_statuses_from_url(request):
    if "status" in request.GET:
        statuses = []
        if request.user.is_authenticated and request.user.is_staff:
            # Staff can view all statuses
            allowed = set(
                map(operator.itemgetter(0), HistoricalActivity.STATUS_CHOICES)
            )
        else:
            allowed = set(HistoricalActivity.PUBLIC_STATUSES)

        for status in request.GET.getlist("status"):
            try:
                status = int(status)
            except (ValueError, TypeError):  # pragma: no cover
                continue

            if status in allowed:
                statuses.append(status)

    else:
        statuses = HistoricalActivity.PUBLIC_STATUSES

    return statuses


def clean_filter_query_string(request):
    whitelist = QueryDict(mutable=True)

    if request.GET:
        for key in request.GET.keys():
            whitelist.setlist(key, request.GET.getlist(key))

    return whitelist


def get_list_element_by_key(the_list, key, value):
    """
    Returns the *first* dictionary in a list whose value of a key matches the given value,
    or None
    """
    if value is not None and not value == "":
        for i, dict_element in enumerate(the_list):
            if dict_element.get(key, None) == value:
                return dict_element, i
    return None, None


def remove_all_dict_keys_from_mixed_dict(maybe_dict, key_name):
    """
    Recursively removes all occurences of one key from a dictionary. The recursion if continued
    in all lists the dictionary contains
    """
    if isinstance(maybe_dict, dict):
        if key_name in maybe_dict:
            del maybe_dict[key_name]
        for obj in maybe_dict.values():
            remove_all_dict_keys_from_mixed_dict(obj, key_name)
    elif isinstance(maybe_dict, list):
        for obj in maybe_dict:
            remove_all_dict_keys_from_mixed_dict(obj, key_name)
