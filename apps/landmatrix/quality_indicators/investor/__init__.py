from django.utils.translation import gettext_lazy as _

from ..dataclass import QualityIndicator
from .queries import *

INVESTOR_QIS: list[QualityIndicator] = [
    QualityIndicator(
        key="name",
        name=_("Investor name given."),
        description=_(
            "Investors for which a valid name is given "
            "(invalid if missing OR = 'unknown' OR = 'unnamed')."
        ),
        query=lambda: q_has_valid_name(),
    ),
    QualityIndicator(
        key="country",
        name=_("Country of origin/registration given."),
        description=_(
            "Investors for which the country of origin/registration is given."
        ),
        query=lambda: q_has_country(),
    ),
    QualityIndicator(
        key="involvements",
        name=_("Investors with at least one involvement."),
        description=_(
            "Investors that are involved in at least one deal or in one investor."
        ),
        query=lambda: q_has_involvement(),
    ),
    QualityIndicator(
        key="data-sources",
        name=_("Data sources files given."),
        description=_(
            "Investors for which all data source files for data sources of "
            "type = contract, "
            "type = contract (contract farming agreement), "
            "type = research paper / policy report, "
            "type = company sources, "
            "type = government sources and "
            "type = media report are given."
        ),
        query=lambda: q_all_data_source_have_file(),
    ),
]
