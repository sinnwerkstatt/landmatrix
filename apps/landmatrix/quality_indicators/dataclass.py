from dataclasses import dataclass
from typing import Callable

from django.db.models import Q


@dataclass
class QualityIndicator:
    key: str
    description: str
    query: Callable[[], Q]


@dataclass
class Subset:
    key: str
    description: str
    query: Callable[[], Q]
