import datetime
import itertools
from typing import Any

from django.utils.duration import duration_iso_string
from django.utils.timezone import is_aware


def qs_values_to_dict(qs, fields, many_to_many_relations=None):
    if not many_to_many_relations:
        many_to_many_relations = []

    def _subkey_expode(target: dict, k, v):
        if "__" not in k:
            target[k] = v
            return
        kx, morekey = k.split("__", 1)
        if not target.get(kx):
            target[kx] = {}
        newtarget = target[kx]
        _subkey_expode(newtarget, morekey, v)

    for related_field in many_to_many_relations:
        related_id_field = f"{related_field}__id"
        if (
            any(f.startswith(related_field) for f in fields)
            and related_id_field not in fields
        ):
            fields += [related_id_field]

    if "id" not in fields:  # we need an ID to group by.
        fields += ["id"]

    qs_values = qs.order_by("id").values(
        *fields,
    )  # needs to be ordered in order to be grouped :S
    grouped_results = itertools.groupby(qs_values, key=lambda value: value["id"])
    results = []

    for _, dealgroup in grouped_results:
        richdeal = {}
        firstround = True
        seen_mtms = {}
        for mtm in many_to_many_relations:
            richdeal[mtm] = []
            seen_mtms[mtm] = set()
        for group in dealgroup:
            manytomany_combine = {mtm: {} for mtm in many_to_many_relations}
            for key, val in group.items():
                if val is None:
                    continue
                if "__" in key:
                    keyprefix, restkey = key.split("__", 1)
                    # many2many / foreign key related
                    if keyprefix in many_to_many_relations:
                        _subkey_expode(manytomany_combine[keyprefix], restkey, val)
                    # foreign key pointer / one2one
                    elif firstround:
                        _subkey_expode(richdeal, key, val)
                elif firstround:
                    richdeal[key] = val

            firstround = False
            for mtm in many_to_many_relations:
                mtm_add = manytomany_combine[mtm]
                if mtm_add and mtm_add["id"] not in seen_mtms[mtm]:
                    richdeal[mtm] += [mtm_add]
                    seen_mtms[mtm].add(mtm_add["id"])
            for mtm in many_to_many_relations:
                richdeal[mtm] = sorted(
                    richdeal[mtm], key=lambda x: x["id"], reverse=True
                )
        results += [richdeal]
    return results


def arrayfield_choices_display(field, choices: tuple) -> list:
    if not field:
        return []
    choices_dict = dict(choices)
    ret = []
    for value in field:
        ret += [str(choices_dict.get(value, value))]
    return ret


def ecma262(o: datetime) -> str:
    if isinstance(o, datetime.datetime):
        r = o.isoformat()
        if o.microsecond:
            r = r[:23] + r[26:]
        if r.endswith("+00:00"):
            r = r[:-6] + "Z"
        return r
    elif isinstance(o, datetime.date):
        return o.isoformat()
    elif isinstance(o, datetime.time):
        if is_aware(o):
            raise ValueError("JSON can't represent timezone-aware times.")
        r = o.isoformat()
        if o.microsecond:
            r = r[:12]
        return r
    elif isinstance(o, datetime.timedelta):
        return duration_iso_string(o)


def set_sensible_fields_to_null(obj: list[Any] | dict[str, Any]):
    fields = ["workflowinfos", "created_by", "modified_by", "current_draft"]
    set_null_recursively(obj, fields)


def set_null_recursively(
    obj: list[Any] | dict[str, Any],
    fields: list[str],
):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in fields:
                obj[key] = None
                continue

            if isinstance(val, (dict, list)):
                set_null_recursively(obj[key], fields)

    if isinstance(obj, list):
        for el in obj:
            if isinstance(el, (dict, list)):
                set_null_recursively(el, fields)
