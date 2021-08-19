from typing import Union

from django.contrib.auth import get_user_model

from apps.landmatrix.models import (
    HistoricalInvestorVentureInvolvement,
    HistoricalInvestor,
)
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from apps.landmatrix.models.gndinvestor import InvestorWorkflowInfo, InvestorVersion
from apps.landmatrix.synchronization.helpers import calculate_new_stati

User = get_user_model()

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
ROLE_MAP = {"ST": "PARENT", "IN": "LENDER"}
INVESTMENT_MAP = {"10": "EQUITY", "20": "DEBT_FINANCING"}
PARENTAL_RELATION_MAP = {
    None: None,
    "Subsidiary": "SUBSIDIARY",
    "Local branch": "LOCAL_BRANCH",
    "Joint venture": "JOINT_VENTURE",
}


def histvestor_to_investor(histvestor: Union[HistoricalInvestor, int]):
    if isinstance(histvestor, int):
        histvestor = HistoricalInvestor.objects.get(id=histvestor)

    investor, created = Investor.objects.get_or_create(
        id=histvestor.investor_identifier,
    )

    investor.name = histvestor.name
    investor.country_id = histvestor.fk_country_id
    investor.classification = (
        CLASSIFICATIONS_MAP[histvestor.classification]
        if histvestor.classification
        else None
    )
    investor.homepage = histvestor.homepage or ""
    investor.opencorporates = histvestor.opencorporates_link or ""
    investor.comment = histvestor.comment or ""

    if created:
        investor.created_at = histvestor.history_date
        investor.created_by = histvestor.history_user
    investor.modified_at = histvestor.history_date
    investor.modified_by = histvestor.history_user
    investor.old_id = histvestor.id

    new_status = histvestor.fk_status_id

    # check involvements
    for involve in HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    ):
        if not Investor.objects.filter(
            id=involve.fk_investor.investor_identifier
        ).exists():
            histvestor_to_investor(involve.fk_investor)

    do_save = investor.status == 1 or new_status in [2, 3, 4]

    old_draft_status = investor.draft_status
    investor.status, investor.draft_status = calculate_new_stati(investor, new_status)
    investor.recalculate_fields()

    involvements = _create_involvements_for_investor(investor, histvestor)

    investor_version = InvestorVersion.from_object(
        investor,
        involvements,
        created_at=histvestor.history_date,
        created_by=histvestor.history_user,
    )
    print(investor_version)
    investor.current_draft = None if new_status in [2, 3, 4] else investor_version

    if do_save:
        # save the actual model
        # if: there is not a current_model
        # or: there is a current model but it's a draft
        # or: the new status is Live, Updated or Deleted
        investor.save()
        InvestorVentureInvolvement.objects.filter(venture=investor).delete()
        InvestorVentureInvolvement.objects.bulk_create(involvements)
    else:
        Investor.objects.filter(pk=investor.pk).update(
            draft_status=investor.draft_status, current_draft=investor_version
        )

    if new_status == 4:
        InvestorVentureInvolvement.objects.filter(venture=investor).delete()

    InvestorWorkflowInfo.objects.create(
        from_user=histvestor.history_user or User.objects.get(id=1),
        draft_status_before=old_draft_status,
        draft_status_after=investor.draft_status,
        timestamp=histvestor.history_date,
        comment=histvestor.action_comment or "",
        processed_by_receiver=True,
        investor=investor,
        investor_version=investor_version,
    )


def _create_involvements_for_investor(investor, histvestor):

    involves = HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    )
    ivis = []
    for histvolvement in involves:
        types = (
            [INVESTMENT_MAP[x] for x in list(histvolvement.investment_type)]
            if histvolvement.investment_type
            else None
        )
        ivi = InvestorVentureInvolvement(
            investor_id=histvolvement.fk_investor.investor_identifier,
            venture_id=investor.id,
            role=ROLE_MAP[histvolvement.role],
            investment_type=types,
            percentage=histvolvement.percentage,
            loans_amount=histvolvement.loans_amount,
            loans_currency_id=histvolvement.loans_currency_id,
            loans_date=histvolvement.loans_date or "",
            parent_relation=PARENTAL_RELATION_MAP[histvolvement.parent_relation],
            comment=histvolvement.comment or "",
            old_id=histvolvement.pk,
        )
        ivis += [ivi]
    return ivis
