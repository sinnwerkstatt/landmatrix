from django.contrib.gis.geos import Point

from apps.landmatrix.models.deal import Deal
from apps.utils import set_sensible_fields_to_null
from .generics import get_foreign_keys


def resolve_deal(_obj, info, id, version=None, subset="PUBLIC"):
    if not user.is_authenticated:
        set_sensible_fields_to_null(deal)

    return deal


def resolve_deals(_obj, info):
    if not user.is_authenticated:
        set_sensible_fields_to_null(results)

    return results


def _clean_payload(payload: dict | None) -> dict:
    ret: dict = {}

    if payload is None:
        return ret

    foreign_keys = get_foreign_keys(Deal)

    for key, value in payload.items():
        if key in foreign_keys:
            if value:
                ret[key] = foreign_keys[key].objects.get(id=value["id"])
        elif key == "point":
            ret["point"] = Point(value["lng"], value["lat"])
        elif key in ["locations", "datasources", "contracts"]:
            new_value = [
                val for val in value if any([v for k, v in val.items() if k != "id"])
            ]
            ret[key] = new_value
        else:
            ret[key] = value
    return ret
