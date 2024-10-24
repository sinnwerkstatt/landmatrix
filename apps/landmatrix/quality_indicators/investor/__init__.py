from django.utils.translation import gettext_lazy as _

from ..dataclass import QualityIndicator
from .queries import *

INVESTOR_QIS: list[QualityIndicator] = [
    QualityIndicator(
        key="name",
        name=_("Name given and not unknown/unnamed."),
        description=_(""),
        query=lambda: q_has_valid_name(),
    ),
    QualityIndicator(
        key="country",
        name=_("Country of origin/registration given."),
        description=_(""),
        query=lambda: q_has_country(),
    ),
    QualityIndicator(
        key="involvements",
        name=_("Involved in at least one deal or with one investor."),
        description=_(""),
        query=lambda: q_has_involvement(),
    ),
    QualityIndicator(
        key="data-sources",
        name=_("Files given for all data sources."),
        description=_(""),
        query=lambda: q_all_data_source_have_file(),
    ),
]
