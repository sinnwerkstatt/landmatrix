from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealHull, DealVersion
from apps.landmatrix.models.investor import (
    InvestorDataSource,
    InvestorHull,
    InvestorVersion,
    Involvement,
)

from .queries import (
    q_has_country,
    q_has_involvement,
    q_all_data_source_have_file,
    q_has_valid_name,
)


def test_q_has_valid_name() -> None:
    investor = InvestorHull.objects.create()

    qs = InvestorVersion.objects.all()

    InvestorVersion.objects.create(investor=investor)
    assert not qs.filter(q_has_valid_name()).exists(), "Invalid: No name specified."

    InvestorVersion.objects.create(investor=investor, name="UnKnOwN")
    assert not qs.filter(q_has_valid_name()).exists(), (
        "Invalid: Name contains 'unknown' (case insensitive)."
    )

    InvestorVersion.objects.create(investor=investor, name="UnNaMeD")
    assert not qs.filter(q_has_valid_name()).exists(), (
        "Invalid: Name contains 'unnamed' (case insensitive)."
    )

    InvestorVersion.objects.create(investor=investor, name="Known Investor")
    InvestorVersion.objects.create(investor=investor, name="Named Investor")

    assert qs.filter(q_has_valid_name()).exists()
    assert qs.filter(q_has_valid_name()).count() == 2


def test_q_has_involvement() -> None:
    parent_investor = InvestorHull.objects.create()
    parent_investor.active_version = InvestorVersion.objects.create(
        investor=parent_investor
    )
    parent_investor.save()

    child_investor = InvestorHull.objects.create()
    child_investor.active_version = InvestorVersion.objects.create(
        investor=child_investor
    )
    child_investor.save()

    assert not InvestorVersion.objects.filter(q_has_involvement()).exists(), (
        "Invalid: No involvement as operating company or investor."
    )

    Involvement.objects.create(
        child_investor=child_investor,
        parent_investor=parent_investor,
    )

    assert InvestorVersion.objects.filter(q_has_involvement()).count() == 1, (
        "Valid: Involvement as investor."
    )

    deal = DealHull.objects.create()
    deal.active_version = DealVersion.objects.create(
        deal=deal,
        operating_company=child_investor,
    )
    deal.save()

    assert InvestorVersion.objects.filter(q_has_involvement()).count() == 2, (
        "Valid: Involvement as operating company."
    )


def test_q_has_country() -> None:
    investor = InvestorHull.objects.create()

    InvestorVersion.objects.create(investor=investor)

    assert not InvestorVersion.objects.filter(q_has_country()).exists(), (
        "Invalid: No country specified."
    )

    InvestorVersion.objects.create(
        investor=investor,
        country=Country.objects.get(name="Spain"),
    )

    assert InvestorVersion.objects.filter(q_has_country()).exists(), (
        "Valid: Country specified."
    )


def test_q_has_valid_data_sources() -> None:
    investor = InvestorHull.objects.create()

    version = InvestorVersion.objects.create(investor=investor)

    assert not InvestorVersion.objects.filter(q_all_data_source_have_file()).exists(), (
        "Invalid: No data sources given."
    )

    InvestorDataSource.objects.create(
        investorversion=version,
        file="document.pdf",
    )
    InvestorDataSource.objects.create(
        investorversion=version,
        file="document2.pdf",
    )

    assert InvestorVersion.objects.filter(q_all_data_source_have_file()).count() == 1, (
        "Valid: All data sources have files."
    )

    InvestorDataSource.objects.create(
        investorversion=version,
        file="",
    )

    assert not InvestorVersion.objects.filter(q_all_data_source_have_file()).exists(), (
        "Invalid: Any data source has no file."
    )
