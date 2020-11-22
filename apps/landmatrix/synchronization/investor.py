from typing import Union

from apps.landmatrix.models import (
    HistoricalInvestorVentureInvolvement,
    HistoricalInvestor,
)
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from apps.landmatrix.models.versions import Revision, Version
from apps.landmatrix.synchronization.helpers import calculate_new_stati

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


def histvestor_to_investor(histvestor: Union[HistoricalInvestor, int]):
    if isinstance(histvestor, int):
        histvestor = HistoricalInvestor.objects.get(id=histvestor)

    investor, created = Investor.objects.get_or_create(
        id=histvestor.investor_identifier,
        defaults={"created_at": histvestor.history_date},
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
    investor.modified_at = histvestor.history_date
    investor.old_id = histvestor.id

    status = histvestor.fk_status_id

    # check involvements
    for involve in HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    ):
        try:
            Investor.objects.get(id=involve.fk_investor.investor_identifier)
        except Investor.DoesNotExist:
            histvestor_to_investor(involve.fk_investor)

    rev1 = Revision.objects.create(
        date_created=histvestor.history_date,
        user=histvestor.history_user,
        comment=histvestor.action_comment or "",
    )

    do_save = not investor or investor.status == 1 or status in [2, 3, 4]

    investor.new_status, investor.new_draft_status = calculate_new_stati(
        investor, status
    )

    if do_save:
        # save the actual model
        # if: there is not a current_model
        # or: there is a current model but it's a draft
        # or: the new status is Live, Updated or Deleted
        investor.save(custom_modification_date=histvestor.history_date)

    Version.create_from_obj(investor, rev1)

    if not do_save:
        # otherwise update the draft_status of the current_model
        Investor.objects.filter(pk=investor.pk).update(
            draft_status=investor.new_draft_status
        )

    _create_involvements_for_investor(investor, histvestor, status, rev1)


def _create_involvements_for_investor(investor, histvestor, do_save, revision):
    if do_save:
        InvestorVentureInvolvement.objects.filter(venture=investor).delete()

    involves = HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    )

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
        if do_save:
            ivi.save()
        Version.create_from_obj(ivi, revision)


ROLE_MAP = {"ST": "PARENT", "IN": "LENDER"}
INVESTMENT_MAP = {"10": "EQUITY", "20": "DEBT_FINANCING"}
PARENTAL_RELATION_MAP = {
    None: None,
    "Subsidiary": "SUBSIDIARY",
    "Local branch": "LOCAL_BRANCH",
    "Joint venture": "JOINT_VENTURE",
}
