import datetime
import itertools

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

    if "id" not in fields:  # we need an ID to group by.
        fields += ["id"]
    qs_values = qs.values(*fields)
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
                    if many_to_many_relations and keyprefix in many_to_many_relations:
                        _subkey_expode(manytomany_combine[keyprefix], restkey, val)
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
