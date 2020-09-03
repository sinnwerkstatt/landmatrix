import itertools


def qs_values_to_dict(qs, fields, many_to_many_relations=None):
    def _subkey_expode(target: dict, k, v):
        if "__" not in k:
            target[k] = v
            return
        kx, morekey = k.split("__", 1)
        if not target.get(kx):
            target[kx] = {}
        newtarget = target[kx]
        _subkey_expode(newtarget, morekey, v)

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
                        manytomany_combine[keyprefix][restkey] = val
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

        results += [richdeal]
    return results
