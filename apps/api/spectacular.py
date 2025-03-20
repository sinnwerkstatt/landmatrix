from collections.abc import Callable, Iterable
from typing import Literal

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

# endpoint = [path, regex_path, method, callback]
Endpoint = tuple[str, str, Method, Callable]

PUBLIC_PATHS: list[str] = [
    "/api/countries/",
    "/api/regions/",
    "/api/currencies/",
    "/api/deals/",
    "/api/investors/",
    "/api/field_choices/",
    "/api/schema/",
]

WAGTAIL_PATHS: list[str] = [
    "/cms/",
    "/api/wagtail/",
]


def is_wagtail(endpoint: Endpoint) -> bool:
    return any(endpoint[0].startswith(x) for x in WAGTAIL_PATHS)


def is_public(endpoint: Endpoint) -> bool:
    return any(endpoint[0].startswith(x) for x in PUBLIC_PATHS)


def is_method(method: Method) -> Callable[[Endpoint], bool]:
    return lambda endpoint: endpoint[2] == method


def preprocess_exclude_wagtail(endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]:
    return filter(lambda x: not is_wagtail(x), endpoints)


def preprocess_only_get(endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]:
    return filter(is_method("GET"), endpoints)


def preprocess_only_public(endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]:
    return filter(is_public, endpoints)
