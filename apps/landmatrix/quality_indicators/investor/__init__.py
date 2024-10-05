from django.utils.translation import gettext_lazy as _

from ..dataclass import QualityIndicator
from .queries import *

INVESTOR_QIS: list[QualityIndicator] = [
    QualityIndicator(
        key="name",
        description=_("Name given and not unknown/unnamed."),
        query=lambda: q_has_valid_name(),
    ),
    QualityIndicator(
        key="country",
        description=_("Country of origin/registration given."),
        query=lambda: q_has_country(),
    ),
    QualityIndicator(
        key="involvements",
        description=_("Involved in at least one deal or with one investor."),
        query=lambda: q_has_involvement(),
    ),
    QualityIndicator(
        key="data-sources",
        description=_("Files given for all data sources."),
        query=lambda: q_all_data_source_have_file(),
    ),
]
