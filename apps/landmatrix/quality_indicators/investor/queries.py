from django.db.models.expressions import OuterRef
from django.db.models.query_utils import Q

from ..data_source.queries import q_has_file
from ..submodel_queries import _q_all, _q_any


def q_has_valid_name() -> Q:
    return ~Q(name="") & ~Q(name__iregex=r"(unnamed|unknown)")


def q_has_involvement() -> Q:
    from apps.landmatrix.models.investor import Involvement
    from apps.landmatrix.models.deal import DealVersion

    return _q_any(
        Involvement.objects.filter(
            parent_investor=OuterRef("investor"),
        ).values("parent_investor")
    ) | _q_any(
        DealVersion.objects.filter(
            operating_company=OuterRef("investor"),
        ).values("operating_company")
    )


def q_has_country() -> Q:
    return Q(country__isnull=False)


def q_all_data_source_have_file() -> Q:
    from apps.landmatrix.models.investor import InvestorDataSource

    return _q_all(
        InvestorDataSource.objects.filter(
            investorversion=OuterRef("pk"),
        ).values("investorversion"),
        q_has_file(),
    )
