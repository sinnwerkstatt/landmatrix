import re

import reversion

from apps.greennewdeal.models import Investor, InvestorVentureInvolvement
from apps.landmatrix.models import HistoricalInvestorVentureInvolvement

CLASSIFICATIONS_MAP = {
    "10": "PRIVATE_COMPANY",
    "20": "STOCK_EXCHANGE_LISTED_COMPANY",
    "30": "INDIVIDUAL_ENTREPRENEUR",
    "40": "INVESTMENT_FUND",
    "170": "INVESTMENT_FUND",
    "50": "SEMI_STATE_OWNED_COMPANY",
    "60": "STATE_OWNED_COMPANY",
    "70": "OTHER",
    "110": "GOVERNMENT",
    "120": "GOVERNMENT_INSTITUTION",
    "130": "MULTILATERAL_DEVELOPMENT_BANK",
    "140": "BILATERAL_DEVELOPMENT_BANK",
    "150": "COMMERCIAL_BANK",
    "160": "INVESTMENT_BANK",
    "180": "INSURANCE_FIRM",
    "190": "PRIVATE_EQUITY_FIRM",
    "200": "ASSET_MANAGEMENT_FIRM",
    "210": "NON_PROFIT",
}

invalid_name = re.compile(
    r"^unknown ?(\(\))? $|^(unknown \()?unnamed (investor|company) ?[0-9]*(\))?$"
)


def hist_to_inv(histvestor):
    investor, created = Investor.objects.get_or_create(
        id=histvestor.investor_identifier
    )

    if not invalid_name.match(histvestor.name.lower()):
        investor.name = histvestor.name

    investor.country_id = histvestor.fk_country_id
    if histvestor.classification:
        investor.classification = CLASSIFICATIONS_MAP[histvestor.classification]
    investor.homepage = histvestor.homepage or ""
    investor.opencorporates = histvestor.opencorporates_link or ""
    investor.comment = histvestor.comment or ""

    status = histvestor.fk_status_id
    investor.timestamp = histvestor.history_date
    investor.old_id = histvestor.id

    # check involvements
    involvs = HistoricalInvestorVentureInvolvement.objects.filter(fk_venture=histvestor)
    for involve in involvs:
        try:
            Investor.objects.get(id=involve.fk_investor.investor_identifier)
        except Investor.DoesNotExist:
            hist_to_inv(involve.fk_investor)

    with reversion.create_revision():
        _create_involvements_for_investor(investor, histvestor)

        investor.save_revision(
            status,
            histvestor.history_date,
            histvestor.history_user,
            histvestor.action_comment or "",
        )


def _create_involvements_for_investor(investor, histvestor):
    InvestorVentureInvolvement.objects.filter(venture=investor).delete()

    involves = HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    )

    for histvolvement in involves:
        ivi = InvestorVentureInvolvement.objects.create(
            investor_id=histvolvement.fk_investor.investor_identifier,
            venture_id=investor.id,
            role=ROLE_MAP[histvolvement.role],
            status=histvolvement.fk_status_id,
        )
        if histvolvement.investment_type:
            types = [INVESTMENT_MAP[x] for x in list(histvolvement.investment_type)]
            ivi.investment_type = types
        ivi.percentage = histvolvement.percentage
        ivi.loans_amount = histvolvement.loans_amount
        ivi.loans_currency_id = histvolvement.loans_currency_id
        ivi.loans_date = histvolvement.loans_date or ""
        ivi.parent_relation = PARENTAL_RELATION_MAP[histvolvement.parent_relation]
        ivi.comment = histvolvement.comment or ""
        ivi.old_id = histvolvement.pk


ROLE_MAP = {"ST": "STAKEHOLDER", "IN": "INVESTOR"}
INVESTMENT_MAP = {"10": "EQUITY", "20": "DEBT_FINANCING"}
PARENTAL_RELATION_MAP = {
    None: None,
    "Subsidiary": "SUBSIDIARY",
    "Local branch": "LOCAL_BRANCH",
    "Joint venture": "JOINT_VENTURE",
}
