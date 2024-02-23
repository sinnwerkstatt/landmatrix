import sys

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import QuerySet
from icecream import ic

from apps.landmatrix.models.investor import (
    InvestorOld,
    InvestorVersion,
    InvestorWorkflowInfoOld,
)
from apps.landmatrix.models.new import (
    InvestorHull,
    InvestorVersion2,
    InvestorDataSource,
    InvestorWorkflowInfo2,
)

status_map_dings = {
    1: "DRAFT",
    2: "REVIEW",
    3: "ACTIVATION",
    4: "REVIEW",
    5: "DRAFT",
    None: None,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("start_id", nargs="?", type=int)
        parser.add_argument("end_id", nargs="?", type=int)

    def handle(self, *args, **options):
        investors: QuerySet[InvestorOld] = (
            InvestorOld.objects.all().order_by("id").all()
        )
        if options["start_id"]:
            investors = investors.filter(id__gte=options["start_id"])
        if options["end_id"]:
            investors = investors.filter(id__lte=options["end_id"])

        for old_investor in investors:
            investor_hull: InvestorHull
            investor_hull, _ = InvestorHull.objects.get_or_create(
                id=old_investor.id,
                first_created_by_id=old_investor.created_by_id or 1,
                first_created_at=old_investor.created_at,
            )

            ic(old_investor.id, old_investor.status)
            for old_version in old_investor.versions.all().order_by("id"):
                ic(old_version)
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

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval('landmatrix_investorhull_id_seq', (SELECT MAX(id) from landmatrix_investorhull))"
            )
            cursor.execute(
                "SELECT setval('landmatrix_investorversion2_id_seq', (SELECT MAX(id) from landmatrix_investorversion2))"
            )
            cursor.execute(
                "SELECT setval('landmatrix_investorworkflowinfo2_id_seq', (SELECT MAX(id) from landmatrix_investorworkflowinfo2))"
            )


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
            new_version.status = "REVIEW"
            # investor_hull.active_version_id = investor_version.id
        else:
            # print("TODO?!", old_version_dict["draft_status"])
            new_version.status = "DELETED"
    elif old_version_dict["status"] == 4:
        if old_version_dict["draft_status"] is None:
            new_version.status = "DRAFT"
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
        if invo["loans_currency"]:
            if isinstance(invo["loans_currency"], int):
                loan_curr = invo["loans_currency"]
            else:
                loan_curr = invo["loans_currency"]["id"]
        else:
            loan_curr = None
        ret += [
            {
                "id": invo["id"],
                "parent_investor_id": invo["investor"],
                "child_investor_id": invo["venture"],
                "role": invo["role"],
                "investment_type": invo["investment_type"] or [],
                "percentage": invo["percentage"],
                "loans_amount": invo["loans_amount"],
                "loans_currency_id": loan_curr,
                "loans_date": invo["loans_date"],
                "parent_relation": invo["parent_relation"] or None,
                "comment": invo["comment"],
            }
        ]
    return ret


def do_workflows(investor_id):
    for wfi_old in InvestorWorkflowInfoOld.objects.filter(investor_id=investor_id):
        wfi_old: InvestorWorkflowInfoOld

        status_before = status_map_dings[wfi_old.draft_status_before]
        status_after = status_map_dings[wfi_old.draft_status_after]
        if status_before in ["REVIEW", "ACTIVATION"] and status_after is None:
            status_after = "ACTIVATED"

        wfi, _ = InvestorWorkflowInfo2.objects.get_or_create(
            id=wfi_old.id,
            defaults={
                "from_user_id": wfi_old.from_user_id,
                "to_user_id": wfi_old.to_user_id,
                "status_before": status_before,
                "status_after": status_after,
                "timestamp": wfi_old.timestamp,
                "comment": wfi_old.comment or "",
                "replies": wfi_old.replies or [],
                "resolved": wfi_old.resolved,
                "investor_id": wfi_old.investor_id,
                "investor_version_id": wfi_old.investor_version_id,
            },
        )

        if not wfi.investor_version_id:
            continue
        dv: InvestorVersion2 = InvestorVersion2.objects.get(id=wfi.investor_version_id)
        if wfi.status_before is None and wfi.status_after == "DRAFT":
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.
        elif (
            wfi.status_before in ["REVIEW", "ACTIVATION"]
            and wfi.status_after == "DRAFT"
        ):
            # ic(
            #     "new draft... what to do?",
            #     wfi.timestamp,
            #     wfi.from_user,
            #     wfi.status_before,
            #     wfi.status_after
            # )
            ...  # TODO I think we're good here. Don't see anything that we ought to be doing.

        elif (wfi.status_before is None and wfi.status_after is None) or (
            wfi.status_before == wfi.status_after
        ):
            ...  # nothing?
        elif (
            wfi.status_before in [None, "DRAFT", "TO_DELETE"]
            and wfi.status_after == "REVIEW"
        ):
            dv.sent_to_review_at = wfi.timestamp
            dv.sent_to_review_by = wfi.from_user
            dv.save()
        elif (
            wfi.status_before in [None, "REVIEW", "TO_DELETE"]
            and wfi.status_after == "ACTIVATION"
        ):
            dv.sent_to_activation_at = wfi.timestamp
            dv.sent_to_activation_by = wfi.from_user
            dv.save()
            # dv.status
        elif (
            wfi.status_before in ["REVIEW", "ACTIVATION"]
            and wfi.status_after == "ACTIVATED"
        ):
            dv.activated_at = wfi.timestamp
            dv.activated_by = wfi.from_user
            dv.save()
        elif wfi.status_before == "REJECTED" or wfi.status_after == "REJECTED":
            dv.modified_at = wfi.timestamp
            dv.save()
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
            sys.exit(1)
        elif wfi.status_after == "TO_DELETE":
            dv.status = "DRAFT"
            dv.save()
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
            sys.exit(1)
        elif wfi.status_before == "TO_DELETE" and wfi.status_after != "TO_DELETE":
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
            sys.exit(1)
        else:
            ...
            ic(
                "DWI OHO",
                wfi.id,
                wfi.timestamp,
                wfi.from_user,
                wfi.investor_id,
                wfi.status_before,
                wfi.status_after,
                wfi.comment,
            )
