from apps.landmatrix.models.choices import DatasourceTypeEnum
from apps.landmatrix.models.deal import DealDataSource

from .queries import q_has_file, q_requires_file


def test_q_requires_file(deal_with_active_version):
    version = deal_with_active_version.active_version

    assert DealDataSource.objects.count() == 0

    for ds_type in DatasourceTypeEnum.values:
        DealDataSource.objects.create(dealversion=version, type=ds_type)

    assert DealDataSource.objects.count() == 9
    assert DealDataSource.objects.filter(q_requires_file()).count() == 6


def test_q_has_file(deal_with_active_version):
    version = deal_with_active_version.active_version

    DealDataSource.objects.create(dealversion=version)

    assert DealDataSource.objects.count() == 1
    assert DealDataSource.objects.filter(q_has_file()).count() == 0

    DealDataSource.objects.create(dealversion=version, file="document.pdf")

    assert DealDataSource.objects.count() == 2
    assert DealDataSource.objects.filter(q_has_file()).count() == 1
