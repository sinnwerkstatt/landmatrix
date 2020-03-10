from apps.greennewdeal.models import Investor, InvestorVentureInvolvement
from apps.landmatrix.models import (
    HistoricalInvestor,
    HistoricalInvestorVentureInvolvement,
)

STATUS_MAP = {1: 1, 2: 2, 3: 2, 4: 4, 5: 5, 6: 6}

ROLE_MAP = {"ST": 10, "IN": 20}

PARENTAL_RELATION_MAP = {
    None: None,
    "Subsidiary": 10,
    "Local branch": 20,
    "Joint venture": 30,
}


def histvestor_to_investor(investor_pk: int = None, investor_identifier: int = None):
    if investor_pk and investor_identifier:
        raise AttributeError("just specify one")
    elif investor_pk:
        histvestor_versions = HistoricalInvestor.objects.filter(pk=investor_pk)
    elif investor_identifier:
        histvestor_versions = HistoricalInvestor.objects.filter(
            investor_identifier=investor_identifier
        ).order_by("pk")
    else:
        raise AttributeError("specify investor_pk or investor_identifier")

    if not histvestor_versions:
        return

    try:
        investor = Investor.objects.get(id=histvestor_versions[0].investor_identifier)
    except Investor.DoesNotExist:
        investor = Investor(id=histvestor_versions[0].investor_identifier)

    for histvestor in histvestor_versions.order_by("pk"):
        investor.name = histvestor.name
        investor.country_id = histvestor.fk_country_id
        if histvestor.classification:
            investor.classification = int(histvestor.classification)
        investor.homepage = histvestor.homepage or ""
        investor.opencorporates = histvestor.opencorporates_link or ""
        investor.comment = histvestor.comment or ""

        status = STATUS_MAP[histvestor.fk_status_id]
        investor.timestamp = histvestor.history_date

        investor.save_revision(
            status,
            histvestor.history_date,
            histvestor.history_user,
            histvestor.action_comment or "",
        )


def histvolvements_to_involvements(ids: list):
    histvolvement_versions = HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture__investor_identifier=ids[0], fk_investor__investor_identifier=ids[1]
    )

    try:
        inv = InvestorVentureInvolvement.objects.get(
            investor_id=ids[1], venture_id=ids[0],
        )
        # TODO: is this the right way round?
    except InvestorVentureInvolvement.DoesNotExist:
        inv = InvestorVentureInvolvement(investor_id=ids[1], venture_id=ids[0])

    for hist_involvement in histvolvement_versions.order_by("pk"):
        inv.role = ROLE_MAP[hist_involvement.role]
        if hist_involvement.investment_type:
            inv.investment_type = list(hist_involvement.investment_type)
        inv.percentage = hist_involvement.percentage
        inv.loans_amount = hist_involvement.loans_amount
        inv.loans_currency_id = hist_involvement.loans_currency_id
        inv.loans_date = hist_involvement.loans_date or ""
        inv.parent_relation = PARENTAL_RELATION_MAP[hist_involvement.parent_relation]
        inv.comment = hist_involvement.comment or ""
        inv.old_id = hist_involvement.pk

        status = STATUS_MAP[hist_involvement.fk_status_id]

        inv.save_revision(status)
