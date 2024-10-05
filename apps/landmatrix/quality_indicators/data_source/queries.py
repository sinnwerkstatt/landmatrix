from django.db.models.query_utils import Q

from apps.landmatrix.models.choices import DatasourceTypeEnum


def q_requires_file() -> Q:
    return Q(
        type__in=[
            DatasourceTypeEnum.MEDIA_REPORT,
            DatasourceTypeEnum.GOVERNMENT_SOURCES,
            DatasourceTypeEnum.CONTRACT,
            DatasourceTypeEnum.CONTRACT_FARMING_AGREEMENT,
            DatasourceTypeEnum.COMPANY_SOURCES,
            DatasourceTypeEnum.RESEARCH_PAPER_OR_POLICY_REPORT,
        ]
    )


def q_has_file() -> Q:
    return ~Q(file="")


def q_has_required_file() -> Q:
    return q_requires_file() & q_has_file()
