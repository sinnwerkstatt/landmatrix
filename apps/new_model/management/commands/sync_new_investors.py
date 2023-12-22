import sys

from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from icecream import ic

from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.landmatrix.models.new import (
    InvestorHull,
    InvestorVersion2,
    InvestorDataSource,
)

status_map_dings = {
    1: "DRAFT",
    2: "REVIEW",
    3: "ACTIVATION",
    4: "REJECTED",
    5: "TO_DELETE",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        investors: QuerySet[Investor] = Investor.objects.all().order_by("id").all()
        for old_investor in investors:
            investor_hull: InvestorHull
            investor_hull, _ = InvestorHull.objects.get_or_create(
                id=old_investor.id,
                # created_by_id=old_investor.created_by_id or 1,
                # created_at=old_investor.created_at,
            )

            ic(old_investor.id, old_investor.status)
            for old_version in old_investor.versions.all().order_by("id"):
                new_version: InvestorVersion2
                base_payload = {
                    "investor_id": old_investor.id,
                    "id": old_version.id,
                    "created_at": old_version.created_at,
                    "created_by_id": old_version.created_by_id,
                    "modified_at": old_version.modified_at,
                    "modified_by_id": old_version.modified_by_id,
                }
                try:
                    new_version = InvestorVersion2.objects.get(**base_payload)
                except InvestorVersion2.DoesNotExist:
                    new_version = InvestorVersion2(**base_payload)

                ov: dict = old_version.serialized_data
                new_version.country_id = ov["country"]
                new_version.name = ov["name"]
                new_version.name_unknown = ov["is_actually_unknown"]
                new_version.classification = ov["classification"]
                new_version.homepage = ov["homepage"]
                new_version.opencorporates = ov["opencorporates"]
                new_version.comment = ov["comment"]
                new_version.involvements_snapshot = _map_involvements_to_new_format(
                    ov["investors"]
                )
                new_version.save()
                if ov.get("datasources"):
                    map_datasources(new_version, ov["datasources"])
                else:
                    new_version.datasources.set([])

                _map_status(investor_hull, new_version, old_version)
                new_version.save()

            investor_hull.deleted = old_investor.status == 4

            do_workflows(old_investor.id)

            investor_hull.save()


def _map_status(investor_hull, new_version, old_version: InvestorVersion):
    old_version_dict = old_version.serialized_data

    if old_version_dict["status"] == 1:
        new_version.status = status_map_dings[old_version_dict["draft_status"]]
        investor_hull.draft_version_id = old_version.id
    elif old_version_dict["status"] in [2, 3]:
        if old_version_dict["draft_status"] is None:
            new_version.status = "ACTIVATED"
            investor_hull.active_version_id = old_version.id
            investor_hull.draft_version_id = None
        elif old_version_dict["draft_status"] == 1:
            new_version.status = "DRAFT"
            investor_hull.draft_version_id = old_version.id
        elif old_version_dict["draft_status"] == 2:
            new_version.status = "REVIEW"
            investor_hull.draft_version_id = old_version.id
        elif old_version_dict["draft_status"] == 3:
            new_version.status = "ACTIVATION"
            investor_hull.draft_version_id = old_version.id
        elif old_version_dict["draft_status"] == 4:
            new_version.status = "REJECTED"
            # investor_hull.active_version_id = investor_version.id
        else:
            # print("TODO?!", old_version_dict["draft_status"])
            new_version.status = "DELETED"
    elif old_version_dict["status"] == 4:
        if old_version_dict["draft_status"] is None:
            new_version.status = "TO_DELETE"
            investor_hull.active_version_id = old_version.id
        else:
            ic("TODO DELETE else?!")
            ...  # TODO !!
    else:
        print("VERSION OHO", old_version.object_id, old_version_dict["status"])


def map_datasources(nv: InvestorVersion2, datasources: list[dict]):
    for dats in datasources:
        ds1, _ = InvestorDataSource.objects.get_or_create(
            investorversion_id=nv.id, nid=dats["id"]
        )
        ds1.type = dats.get("type", "")
        ds1.url = dats.get("url", "")
        if dats.get("file"):
            ds1.file.name = dats["file"]
        ds1.file_not_public = dats.get("file_not_public", False)
        ds1.publication_title = dats.get("publication_title", "")
        ds1.date = dats.get("date")
        ds1.name = dats.get("name", "")
        ds1.company = dats.get("company", "")
        ds1.email = dats.get("email", "")
        ds1.phone = dats.get("phone", "")
        ds1.includes_in_country_verified_information = dats.get(
            "includes_in_country_verified_information", ""
        )
        ds1.open_land_contracts_id = dats.get("open_land_contracts_id", "")
        ds1.comment = dats.get("comment", "")
        ds1.save()


def _map_involvements_to_new_format(invos: list) -> list:
    if not invos:
        return []
    ret = []
    for invo in invos:
        ret += [
            {
                "id": invo["id"],
                "parent_investor_id": invo["investor"],
                "child_investor_id": invo["venture"],
                "role": invo["role"],
                "investment_type": invo["investment_type"] or [],
                "percentage": invo["percentage"],
                "loans_amount": invo["loans_amount"],
                "loans_currency": invo["loans_currency"],
                "loans_date": invo["loans_date"],
                "parent_relation": invo["parent_relation"] or None,
                "comment": invo["comment"],
            }
        ]
    return ret


def do_workflows(investor_id):
    for wfi in InvestorWorkflowInfo.objects.filter(investor_id=investor_id):
        if not wfi.investor_version_id:
            continue
        dv: InvestorVersion2 = InvestorVersion2.objects.get(id=wfi.investor_version_id)
        if wfi.draft_status_before is None and wfi.draft_status_after == 1:
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.
        elif wfi.draft_status_before in [2, 3] and wfi.draft_status_after == 1:
            # ic(
            #     "new draft... what to do?",
            #     wfi.timestamp,
            #     wfi.from_user,
            #     wfi.draft_status_before,
            #     wfi.draft_status_after
            # )
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.

        elif (wfi.draft_status_before is None and wfi.draft_status_after is None) or (
            wfi.draft_status_before == wfi.draft_status_after
        ):
            ...  # nothing?
        elif wfi.draft_status_before in [None, 1, 5] and wfi.draft_status_after == 2:
            dv.sent_to_review_at = wfi.timestamp
            dv.sent_to_review_by = wfi.from_user
            dv.save()
        elif wfi.draft_status_before in [None, 2, 5] and wfi.draft_status_after == 3:
            dv.sent_to_activation_at = wfi.timestamp
            dv.sent_to_activation_by = wfi.from_user
            dv.save()
            # dv.status
        elif wfi.draft_status_before in [2, 3] and wfi.draft_status_after is None:
            dv.activated_at = wfi.timestamp
            dv.activated_by = wfi.from_user
            dv.save()
        elif wfi.draft_status_before == 4 or wfi.draft_status_after == 4:
            ...  # TODO REJECTED status change
            # ic(
            #     "DWI OHO",
            #     wfi.id,
            #     wfi.timestamp,
            #     wfi.from_user,
            #     wfi.investor_id,
            #     wfi.draft_status_before,
            #     wfi.draft_status_after,z
            #     wfi.comment,
            # )
            # sys.exit(1)
        elif wfi.draft_status_after == 5:
            dv.status = "TO_DELETE"
            dv.save()
        elif wfi.draft_status_before == 5 and wfi.draft_status_after != 5:
            if not wfi.draft_status_after:
                # TODO What is going on here?
                ...
            else:
                dv.status = status_map_dings[wfi.draft_status_after]
                dv.save()
        else:
            ...
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.draft_status_before,
                wfi.draft_status_after,
                wfi.comment,
            )
            sys.exit(1)
