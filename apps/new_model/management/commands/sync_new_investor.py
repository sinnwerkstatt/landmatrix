from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from icecream import ic

from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.new_model.models import (
    InvestorHull,
    InvestorVersion2,
    InvestorDataSource,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        investors: QuerySet[Investor] = Investor.objects.all().order_by("id").all()[:10]
        for old_investor in investors:
            investor_hull: InvestorHull
            investor_hull, _ = InvestorHull.objects.get_or_create(
                id=old_investor.id,
                created_by=old_investor.created_by,
                created_at=old_investor.created_at,
            )

            print(old_investor.id, "status:", old_investor.status)
            for old_dv in old_investor.versions.all().order_by("id"):
                old_dv_dict = old_dv.serialized_data
                new_version: InvestorVersion2
                try:
                    new_version = InvestorVersion2.objects.get(
                        investor_id=old_investor.id, id=old_dv.id
                    )
                except InvestorVersion2.DoesNotExist:
                    new_version = InvestorVersion2(
                        investor_id=old_investor.id, id=old_dv.id
                    )

                map_version_payload(old_dv, new_version)
                # investor_hull.country_id = old_dv_dict["country"]

                if old_dv_dict["status"] == 1:
                    map_dings = {
                        1: "DRAFT",
                        2: "REVIEW",
                        3: "ACTIVATION",
                        4: "REJECTED",
                        5: "TO_DELETE",
                    }
                    new_version.status = map_dings[old_dv_dict["draft_status"]]
                    investor_hull.draft_version_id = old_dv.id
                elif old_dv_dict["status"] in [2, 3]:
                    if old_dv_dict["draft_status"] is None:
                        new_version.status = "ACTIVATED"
                        investor_hull.active_version_id = old_dv.id
                        investor_hull.draft_version_id = None
                    elif old_dv_dict["draft_status"] == 1:
                        new_version.status = "DRAFT"
                        investor_hull.draft_version_id = old_dv.id
                    elif old_dv_dict["draft_status"] == 2:
                        new_version.status = "REVIEW"
                        investor_hull.draft_version_id = old_dv.id
                    elif old_dv_dict["draft_status"] == 3:
                        new_version.status = "ACTIVATION"
                        investor_hull.draft_version_id = old_dv.id
                    elif old_dv_dict["draft_status"] == 4:
                        new_version.status = "REJECTED"
                        # investor_hull.active_version_id = investor_version.id
                    else:
                        # print("TODO?!", old_dv_dict["draft_status"])
                        new_version.status = "DELETED"
                elif old_dv_dict["status"] == 4:
                    if old_dv_dict["draft_status"] is None:
                        new_version.status = "TO_DELETE"
                        investor_hull.active_version_id = old_dv.id
                    else:
                        print("TODO DELETE else?!")
                        ...  # TODO !!
                else:
                    print("VERSION OHO", old_investor.id, old_dv_dict["status"])
                    # return
                # print(old_dv.workflowinfos.all())
                new_version.save()

            # investor_hull.draft_version_id = old_investor.current_draft_id
            investor_hull.deleted = old_investor.status == 4

            do_workflows(old_investor.id)

            investor_hull.save()
            # return


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


def map_version_payload(old_investor_version: InvestorVersion, nv: InvestorVersion2):
    ov: dict = old_investor_version.serialized_data
    nv.country_id = ov["country"]
    nv.name = ov["name"]
    nv.classification = ov["classification"]
    nv.homepage = ov["homepage"]
    nv.opencorporates = ov["opencorporates"]
    nv.comment = ov["comment"]
    nv.save()
    if ov.get("datasources"):
        map_datasources(nv, ov["datasources"])

    nv.created_by_id = old_investor_version.created_by_id
    nv.created_at = old_investor_version.created_at


def do_workflows(investor_id):
    for wfi in InvestorWorkflowInfo.objects.filter(investor_id=investor_id):
        if not wfi.investor_version_id:
            continue
        dv: InvestorVersion2 = InvestorVersion2.objects.get(id=wfi.investor_version_id)
        if wfi.draft_status_before is None and wfi.draft_status_after == 1:
            ic("new draft.. what to do?")
            ...  # TODO new draft.. what to do?
        elif wfi.draft_status_before in [2, 3] and wfi.draft_status_after == 1:
            ic("new draft.. what to do?")
            ...  # TODO new draft.. what to do?
        elif (wfi.draft_status_before is None and wfi.draft_status_after is None) or (
            wfi.draft_status_before == wfi.draft_status_after
        ):
            ...  # nothing?
        elif wfi.draft_status_before in [None, 1] and wfi.draft_status_after == 2:
            dv.sent_to_review_at = wfi.timestamp
            dv.sent_to_review_by = wfi.from_user
            dv.save()
        elif wfi.draft_status_before == 2 and wfi.draft_status_after == 3:
            dv.reviewed_at = wfi.timestamp
            dv.reviewed_by = wfi.from_user
            dv.save()
            # dv.status
        elif wfi.draft_status_before in [2, 3] and wfi.draft_status_after is None:
            dv.activated_at = wfi.timestamp
            dv.activated_by = wfi.from_user
            dv.save()
        elif wfi.draft_status_before == 4 or wfi.draft_status_after == 4:
            ...  # deleted status change
        else:
            ...
            print(
                "DWI OHO",
                wfi.investor_id,
                wfi.draft_status_before,
                wfi.draft_status_after,
                wfi.comment,
            )
