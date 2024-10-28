from django.db.models import QuerySet
from django.db.models.expressions import F, Func, OuterRef, RawSQL
from django.db.models.fields import BooleanField, IntegerField
from django.db.models.functions import JSONObject
from django.db.models.query_utils import Q

from apps.landmatrix.models.choices import AreaTypeEnum

from ..data_source.queries import q_has_required_file, q_requires_file
from ..submodel_queries import _q_all, _q_any, _q_multiple
from .location.queries import (
    q_is_georeferenced,
    q_is_georeferenced_as,
    q_is_high_accuracy,
)


### Location subqueries
def qs_location_subquery() -> QuerySet["Location"]:
    from apps.landmatrix.models.deal import Location

    return Location.objects.filter(
        dealversion=OuterRef("pk"),
    ).values("dealversion")


def q_any_location_georeferenced_or_high_accuracy() -> Q:
    return _q_any(
        qs_location_subquery(),
        q_is_georeferenced() | q_is_high_accuracy(),
    )


def q_all_location_georeferenced_or_high_accuracy() -> Q:
    return _q_all(
        qs_location_subquery(),
        q_is_georeferenced() | q_is_high_accuracy(),
    )


def q_any_location_georeferenced() -> Q:
    return _q_any(
        qs_location_subquery(),
        q_is_georeferenced(),
    )


def q_all_location_georeferenced() -> Q:
    return _q_all(
        qs_location_subquery(),
        q_is_georeferenced(),
    )


def q_any_location_georeferenced_as_contract() -> Q:
    return _q_any(
        qs_location_subquery(),
        q_is_georeferenced_as(AreaTypeEnum.contract_area),
    )


def q_any_location_georeferenced_as_production() -> Q:
    return _q_any(
        qs_location_subquery(),
        q_is_georeferenced_as(AreaTypeEnum.production_area),
    )


### data source subqueries
def qs_data_source_subquery():
    from apps.landmatrix.models.deal import DealDataSource

    return DealDataSource.objects.filter(
        dealversion=OuterRef("pk"),
    ).values("dealversion")


def q_multiple_datasource() -> Q:
    return _q_multiple(qs_data_source_subquery())


def q_all_datasource_valid() -> Q:
    return _q_all(
        qs_data_source_subquery().filter(q_requires_file()),
        q_has_required_file(),
    )


#### deal version
# NOTE: The following require an annotated set of versions like
# DealVersion.objects.annotate(counts=annotate_counts())
def q_all_status() -> Q:
    return Q(
        counts__negotiation_status__total__gt=0,
        counts__implementation_status__total__gt=0,
    )


def q_all_status_dated() -> Q:
    return Q(
        counts__negotiation_status__dated__gt=0,
        counts__implementation_status__dated__gt=0,
    )


def q_any_area_dated() -> Q:
    return Q(counts__production_size__dated__gt=0) | Q(
        counts__contract_size__dated__gt=0
    )


def q_all_status_dated_and_any_area_dated() -> Q:
    return q_any_area_dated() & q_all_status_dated()


def q_any_produce_info() -> Q:
    return Q(JSONFieldAnyValueGreaterZero("counts__produce"))


def q_all_basic_fields() -> Q:
    return (
        Q(
            counts__contract_size__total__gt=0,
            counts__intention_of_investment__total__gt=0,
            counts__negotiation_status__total__gt=0,
            counts__implementation_status__total__gt=0,
            counts__nature_of_deal__gt=0,
        )
        & q_any_produce_info()
    )


def q_operating_company_in_target_country() -> Q:
    return Q(deal__country=F("operating_company__active_version__country"))


### helpers
def annotate_counts() -> JSONObject:
    return JSONObject(
        intention_of_investment=json_field_counts("intention_of_investment"),
        negotiation_status=json_field_counts("negotiation_status"),
        implementation_status=json_field_counts("implementation_status"),
        production_size=json_field_counts("production_size"),
        contract_size=json_field_counts("contract_size"),
        nature_of_deal=ArrayLength("nature_of_deal"),
        produce=produce_counts(),  # this counts all produce related fields separately
    )


def produce_counts() -> JSONObject:
    return JSONObject(
        **{
            produce: JSONArrayLength(produce)
            for produce in [
                "crops",
                "animals",
                "mineral_resources",
                "contract_farming_crops",
                "contract_farming_animals",
                "electricity_generation",
                "carbon_sequestration",
            ]
        }
    )


def json_field_counts(field_name: str) -> JSONObject:
    return JSONObject(
        total=JSONArrayLength(field_name),
        dated=count_dated(field_name),
    )


# TODO: test me
def count_dated(json_field_name: str) -> RawSQL:
    return RawSQL(
        f"""
        jsonb_array_length(
            jsonb_path_query_array({json_field_name}, '$? (@.date != null)')
        )
        """,
        [],
        output_field=IntegerField(),
    )


# https://www.postgresql.org/docs/16/functions-json.html
class JSONArrayLength(Func):
    function = "jsonb_array_length"


# https://www.postgresql.org/docs/16/functions-array.html
class ArrayLength(Func):
    function = "CARDINALITY"


class JSONFieldAnyValueGreaterZero(Func):
    function = "EXISTS"
    template = """%(function)s (
        SELECT 1
        FROM jsonb_each_text(%(expressions)s) AS kv(key, value)
        WHERE kv.value::int > 0
    )"""
    output_field = BooleanField()
