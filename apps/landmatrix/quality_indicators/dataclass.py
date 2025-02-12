from collections.abc import Callable
from dataclasses import dataclass

from django.db.models import Q


@dataclass
class QualityIndicator:
    key: str
    name: str
    description: str
    query: Callable[[], Q]


@dataclass
class Subset:
    key: str
    description: str
    query: Callable[[], Q]
