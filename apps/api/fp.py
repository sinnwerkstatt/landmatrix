from typing import Any, Callable, Iterable, Optional, ParamSpec, TypeVar

# sry @all I had to play around :)
P = ParamSpec("P")

T = TypeVar("T")
T2 = TypeVar("T2")


### iterable
def _filter(fn: Callable[[T], bool]) -> Callable[[Iterable[T]], Iterable[T]]:
    def wrapper(iterable: Iterable[T]) -> Iterable[T]:
        return filter(fn, iterable)

    return wrapper
    # return lambda iterable: filter(fn, iterable)


def _map(fn: Callable[[T], T2]) -> Callable[[Iterable[T]], Iterable[T2]]:
    def wrapper(iterable: Iterable[T]) -> Iterable[T2]:
        return map(fn, iterable)

    return wrapper
    # return lambda iterable: map(fn, iterable)


### bool
def _and(fn1: Callable[P, bool], fn2: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return fn1(*args, **kwargs) and fn2(*args, **kwargs)

    return wrapper
    # return lambda *args, **kwargs: fn1(*args, **kwargs) and fn2(*args, **kwargs)


def _or(fn1: Callable[P, bool], fn2: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return fn1(*args, **kwargs) or fn2(*args, **kwargs)

    return wrapper
    # return lambda *args, **kwargs: fn1(*args, **kwargs) or fn2(*args, **kwargs)


def _not(fn: Callable[P, bool]) -> Callable[P, bool]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> bool:
        return not fn(*args, **kwargs)

    return wrapper
    # return lambda *args, **kwargs: not fn(*args, **kwargs)


def _any(fn: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
    def wrapper(iterable: Iterable[T]) -> bool:
        return any(map(fn, iterable))

    return wrapper
    # return lambda iterable: any(map(fn, iterable))


def _all(fn: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
    def wrapper(iterable: Iterable[T]) -> bool:
        return all(map(fn, iterable))

    return wrapper
    # return lambda iterable: all(map(fn, iterable))


### composition
def _pipe2(fn1: Callable[P, T], fn2: Callable[[T], T2]) -> Callable[P, T2]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T2:
        return fn2(fn1(*args, **kwargs))

    return wrapper
    # return lambda *args, **kwargs: fn2(fn1(*args, **kwargs))


def _compose2(fn1: Callable[[T], T2], fn2: Callable[P, T]) -> Callable[P, T2]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T2:
        return fn1(fn2(*args, **kwargs))

    return wrapper
    # return lambda *args, **kwargs: fn1(fn2(*args, **kwargs))


### comparison (literal and deep nested)
def _equals(obj1: T) -> Callable[[T], bool]:
    def wrapper(obj2: T) -> bool:
        return obj1 == obj2

    return wrapper
    # return lambda obj2: obj1 == obj2


# NOTE: nonsense in functional programming, nothing SHOULD have the same reference
def _is(obj1: T) -> Callable[[T], bool]:
    def wrapper(obj2: T) -> bool:
        return obj1 is obj2

    return wrapper
    # return lambda obj2: obj1 is obj2


### unsafe / maybe
# TODO: Fix typing
# NOTE: Python types currently not able to introspect T's attributes in a `keyof T`-like manner
def _getattr(name: str) -> Callable[[T], Optional[Any]]:
    def wrapper(obj: T) -> Optional[Any]:
        return getattr(obj, name, None)

    return wrapper
    # return lambda obj: getattr(obj, name, None)
