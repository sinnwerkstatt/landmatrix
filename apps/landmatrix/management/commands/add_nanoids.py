from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import Deal

from nanoid import generate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for deal in Deal.objects.all().order_by("id"):
            print(deal.id, end="")
            updated = False

            # datasources and contracts
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
            # #####################################

            for x in deal.locations:
                updated = True
                if not x.get("id") or isinstance(x["id"], int):
                    x["old_id"] = x.get("id")
                    x["id"] = generate(size=8)
                if x.get("areas"):
                    for feat in x["areas"].get("features"):
                        if (
                            isinstance(feat["properties"]["id"], str)
                            and len(feat["properties"]["id"]) == 8
                        ):
                            continue
                        # live_id = [
                        #     y
                        #     for y in deal.locations
                        #     if y["old_id"] == feat["properties"]["id"]
                        # ][0]["id"]
                        feat["properties"]["id"] = x["id"]

            if updated:
                print(" - updated", end="")
                deal.save()

            if deal.current_draft:
                ddata = deal.current_draft.serialized_data
                # datasources and contracts
                # print(json.dumps(ddata["datasources"], indent=2))
                # print(json.dumps(deal.datasources, indent=2))
                for x in ddata["datasources"]:
                    if not x.get("id") or isinstance(x["id"], int):
                        if not x.get("id"):
                            x["id"] = generate(size=8)
                            continue
                        if x["id"] in [y["id"] for y in deal.datasources]:
                            print("found ID")
                            continue
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
                        if not x.get("id"):
                            x["id"] = generate(size=8)
                            continue
                        if x["id"] in [y["id"] for y in deal.contracts]:
                            continue
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
                # #####################################

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
                            feat["properties"]["id"] = x["id"]
                if updated:
                    print(" - draft updated", end="")
                    deal.current_draft.save()

            print()
