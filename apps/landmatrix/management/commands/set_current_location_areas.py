from tqdm import tqdm

from django.core.management import BaseCommand

from apps.api.utils.geojson import (
    add_properties,
    create_feature_collection,
    is_geometry_type,
)

from ...models.deal import DealOld, DealVersionOld


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Set current on area feature if not ambiguous."""
        print("Iterating Deals")
        for d in tqdm(
            DealOld.objects.iterator(),
            total=DealOld.objects.count(),
        ):
            d.locations = [fix_current(location) for location in d.locations]
            d.save()

        print("Iterating DealVersions")
        for v in tqdm(
            DealVersionOld.objects.iterator(),
            total=DealVersionOld.objects.count(),
        ):
            v.serialized_data["locations"] = [
                fix_current(location) for location in v.serialized_data["locations"]
            ]
            v.save()

        print("Done")


def fix_current(location):
    areas = location.get("areas")
    if not areas:
        return location

    features = areas.get("features")
    if not features:
        return location

    # discarding all point features (they are duplicates of the location.point)
    features = [f for f in features if not is_geometry_type("Point", f)]

    new_features = []
    for area_type in ["production_area", "contract_area", "intended_area"]:
        area_features = [f for f in features if f["properties"]["type"] == area_type]
        if len(area_features) == 1:  # unambiguous
            new_features += [add_properties({"current": True}, area_features[0])]
        else:  # do nothing
            new_features += area_features

    return {
        **location,
        "areas": create_feature_collection(new_features),
    }
