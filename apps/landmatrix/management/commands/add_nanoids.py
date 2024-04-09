from nanoid import generate

from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import DealOld
from apps.landmatrix.models.investor import InvestorOld


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Deals and deal versions.")
        # ToDo: Change DealOld?!
        for deal in DealOld.objects.all().order_by("id"):
            updated = False

            for x in deal.datasources:
                if not x.get("id") or isinstance(x["id"], int):
                    updated = True
                    x["old_id"] = x.get("id")
                    x["id"] = generate(size=8)

            for x in deal.contracts:
                if not x.get("id") or isinstance(x["id"], int):
                    updated = True
                    x["old_id"] = x.get("id")
                    x["id"] = generate(size=8)

            for x in deal.locations:
                if not x.get("id") or isinstance(x["id"], int):
                    updated = True
                    x["old_id"] = x.get("id")
                    x["id"] = generate(size=8)
                if x.get("areas"):
                    for feat in x["areas"].get("features"):
                        if (
                            isinstance(feat["properties"]["id"], str)
                            and len(feat["properties"]["id"]) == 8
                        ):
                            continue
                        updated = True
                        feat["properties"]["id"] = x["id"]

            if updated:
                print(f"{deal.id} - updated")
                deal.save()

            for deal_version in deal.versions.all().order_by("id"):
                updated = False
                ddata = deal_version.serialized_data
                for x in ddata["datasources"]:
                    if not x.get("id") or isinstance(x["id"], int):
                        updated = True
                        try:
                            live_id = [
                                y
                                for y in deal.datasources
                                if y.get("old_id") == x.get("id")
                            ][0]["id"]
                        except IndexError:
                            live_id = generate(size=8)
                        x["id"] = live_id

                for x in ddata["contracts"]:
                    if not x.get("id") or isinstance(x["id"], int):
                        updated = True
                        try:
                            live_id = [
                                y
                                for y in deal.contracts
                                if y.get("old_id") == x.get("id")
                            ][0]["id"]
                        except IndexError:
                            live_id = generate(size=8)
                        x["id"] = live_id

                for x in ddata["locations"]:
                    if not x.get("id") or isinstance(x["id"], int):
                        updated = True
                        try:
                            live_id = [
                                y
                                for y in deal.locations
                                if y.get("old_id") == x.get("id")
                            ][0]["id"]
                        except IndexError:
                            live_id = generate(size=8)
                        x["id"] = live_id
                    if x.get("areas"):
                        for feat in x["areas"].get("features"):
                            if (
                                isinstance(feat["properties"]["id"], str)
                                and len(feat["properties"]["id"]) == 8
                            ):
                                continue
                            updated = True
                            feat["properties"]["id"] = x["id"]

                if updated:
                    print(f"{deal.id} - {deal_version.id} updated")
                    deal_version.save()

        print("Investors and investor versions.")
        # ToDo?!
        for investor in InvestorOld.objects.all().order_by("id"):
            updated = False

            for x in investor.datasources:
                if not x.get("id") or isinstance(x["id"], int):
                    updated = True
                    x["old_id"] = x.get("id")
                    x["id"] = generate(size=8)

            if updated:
                print(f"{investor.id} - updated")
                investor.save()

            for investor_version in investor.versions.all().order_by("id"):
                updated = False
                ddata = investor_version.serialized_data

                if not ddata.get("datasources"):
                    continue

                for x in ddata["datasources"]:
                    if not x.get("id") or isinstance(x["id"], int):
                        updated = True
                        try:
                            live_id = [
                                y
                                for y in investor.datasources
                                if y.get("old_id") == x.get("id")
                            ][0]["id"]
                        except IndexError:
                            live_id = generate(size=8)
                        x["id"] = live_id

                if updated:
                    print(f"{investor.id} - {investor_version.id} updated")
                    investor_version.save()
