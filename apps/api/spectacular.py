from typing import Callable, Iterable, Literal, NamedTuple, ParamSpec

PUBLIC_PATHS: list[str] = [
    "/api/countries/",
    "/api/regions/",
    "/api/currencies/",
    "/api/deals/",
    "/api/deals/{pk}/",
    "/api/deals/{pk}/{version_id}/",
    "/api/investors/",
    "/api/investors/{pk}/",
    "/api/investors/{pk}/{version_id}/",
    "/api/field_choices/",
    "/api/schema/",
]

WAGTAIL_PATHS: list[str] = [
    "/cms/",
    "/api/wagtail/",
]


class Endpoint(NamedTuple):
    path: str
    regex_path: str
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    callback: Callable


def is_wagtail(endpoint: Endpoint) -> bool:
    path = endpoint[0]
    return any(path.startswith(x) for x in WAGTAIL_PATHS)


def is_public(endpoint: Endpoint) -> bool:
    path = endpoint[0]
    return any(path.startswith(x) for x in PUBLIC_PATHS)


def is_get_method(endpoint: Endpoint) -> bool:
    method = endpoint[2]
    return method == "GET"


def production_filters(endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]:
    return filter(_and(is_public, is_get_method), endpoints)


def development_filters(endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]:
    return filter(_not(is_wagtail), endpoints)


# sry @all I had to play around :)
P = ParamSpec("P")


def _and(fn1: Callable[P, bool], fn2: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return fn1(*args, **kwargs) and fn2(*args, **kwargs)

    return wrapper


def _or(fn1: Callable[P, bool], fn2: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return fn1(*args, **kwargs) or fn2(*args, **kwargs)

    return wrapper


def _not(fn: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return not fn(*args, **kwargs)

    return wrapper
