from typing import Iterable, Protocol

from apps.api.fp import _filter, _not, _pipe2
from apps.api.spectacular import Endpoint, is_method, is_public, is_wagtail


# NOTE: endpoints is kwarg!
class PreprocessHook(Protocol):
    def __call__(self, *, endpoints: Iterable[Endpoint]) -> Iterable[Endpoint]: ...


as_positional_arg = lambda endpoints: endpoints


preprocess_exclude_wagtail: PreprocessHook = _pipe2(
    as_positional_arg,
    _filter(_not(is_wagtail)),
)

preprocess_only_get: PreprocessHook = _pipe2(
    as_positional_arg,
    _filter(is_method("GET")),
)

preprocess_only_public: PreprocessHook = _pipe2(
    as_positional_arg,
    _filter(is_public),
)
