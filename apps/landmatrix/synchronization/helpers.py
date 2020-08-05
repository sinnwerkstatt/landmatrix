from collections import defaultdict
from typing import Optional

from apps.landmatrix.models import Contract, DataSource, Deal, Location


def _to_nullbool(val: Optional[str]):
    return None if val is None else val in {"True", "Yes"}


def _extras_to_json(
    attr,
    field,
    val2name: str = None,
    expected_type=str,
    fieldmap=None,
    multi_value=False,
):
    adict = attr.get_dict(field)

    if not adict or not adict["value"]:
        return None

    # NOTE Fixes for broken data
    if expected_type == float and adict["value"] in ("7,8", "101171,5"):
        adict["value"] = adict["value"].replace(",", ".")

    if fieldmap:
        ret = [{"value": fieldmap[adict["value"]]}]
    else:
        ret = [{"value": expected_type(adict["value"])}]

    if adict["date"]:
        ret[0]["date"] = adict["date"]

    if adict["is_current"]:
        ret[0]["current"] = adict["is_current"]

    if val2name and adict["value2"]:
        ret[0][val2name] = adict["value2"]

    if adict.get("extras"):
        for extra in adict["extras"]:
            if not extra or not extra["value"]:
                continue
            # NOTE Fixes for broken data # deal 618 contract_size
            if expected_type == float and extra["value"] == "":
                continue
            if fieldmap:
                extra_ret = {
                    "value": fieldmap[extra["value"]],
                }
            else:
                extra_ret = {"value": expected_type(extra["value"])}
            if extra["date"]:
                extra_ret["date"] = extra["date"]
            if extra["is_current"]:
                extra_ret["current"] = extra["is_current"]
            if val2name and extra["value2"]:
                extra_ret[val2name] = extra["value2"]
            ret += [extra_ret]
    if multi_value:
        mret = {}
        for x in ret:
            try:
                mret[(x.get("date"), x.get(val2name), x.get("current"))] += [x["value"]]
            except KeyError:
                mret[(x.get("date"), x.get(val2name), x.get("current"))] = [x["value"]]
        fret = []
        for keys, values in mret.items():
            date, val2, current = keys
            add_entry = {"value": values}
            if date:
                add_entry["date"] = date
            if val2:
                add_entry[val2name] = val2
            if current:
                add_entry["current"] = True
            fret += [add_entry]
        ret = fret
    return ret


def _extras_to_list(attr, field: str, mapping: dict):
    adict = attr.get_dict(field)

    if not adict or not adict["value"]:
        return None

    ret = [mapping[adict["value"]]]

    if adict.get("extras"):
        for extra in adict["extras"]:
            ret += [mapping[extra["value"]]]
    return ret


class OldGroup:
    def __init__(self):
        self.attrs = {}

    def update(self, attrs):
        self.activity_id = attrs.fk_activity_id
        if attrs.name in self.attrs.keys():
            try:
                self.attrs[attrs.name]["extras"] += [attrs.to_dict()]
            except KeyError:
                self.attrs[attrs.name]["extras"] = [attrs.to_dict()]
        else:
            self.attrs[attrs.name] = attrs.to_dict()

    def __repr__(self):
        return f"OldGroup: {self.attrs.keys()}"

    def get(self, key, valfield="value"):
        try:
            ret = self.attrs[key]
        except KeyError:
            return None
        return ret[valfield]

    def get_dict(self, key):
        try:
            return self.attrs[key]
        except KeyError:
            return None


class MetaActivity:
    def __init__(self, activity):
        # self.activity: HistoricalActivity = activity

        self.loc_groups = defaultdict(OldGroup)
        self.con_groups = defaultdict(OldGroup)
        self.ds_groups = defaultdict(OldGroup)

        self.group_general = OldGroup()
        self.group_employment = OldGroup()
        self.group_investor_info = OldGroup()
        self.group_local_communities = OldGroup()
        self.group_former_use = OldGroup()
        self.group_produce_info = OldGroup()
        self.group_water = OldGroup()
        self.group_remaining = OldGroup()

        for attr in activity.attributes.all():
            # Locations
            if attr.name in Location.old_attribute_names():
                self.loc_groups[attr.fk_group_id].update(attr)

            # Contracts
            elif attr.name in Contract.old_attribute_names():
                self.con_groups[attr.fk_group_id].update(attr)

            # DataSources
            elif attr.name in DataSource.old_attribute_names():
                self.ds_groups[attr.fk_group_id].update(attr)

            # Deal
            elif attr.name in Deal.old_attribute_names("general"):
                self.group_general.update(attr)
            elif attr.name in Deal.old_attribute_names("employment"):
                self.group_employment.update(attr)
            elif attr.name in Deal.old_attribute_names("investor_info"):
                self.group_investor_info.update(attr)
            elif attr.name in Deal.old_attribute_names("local_communities"):
                self.group_local_communities.update(attr)
            elif attr.name in Deal.old_attribute_names("former_use"):
                self.group_former_use.update(attr)
            elif attr.name in Deal.old_attribute_names("produce_info"):
                self.group_produce_info.update(attr)
            elif attr.name in Deal.old_attribute_names("water"):
                self.group_water.update(attr)
            elif attr.name in Deal.old_attribute_names("remaining"):
                self.group_remaining.update(attr)
            elif attr.name in Deal.old_attribute_names("meta"):
                self.group_remaining.update(attr)  # parse this in remaining.

            elif attr.name in [
                "minerals_export",
                "old_contract_area",
                "old_production_area",
                "old_reliability_ranking",
                "previous_identifier",
                "terms",
                "Remark (Benefits for local communities)",
                "Remark (Nature of the deal)",
                "Remark (Number of Jobs Created)",
                "original_filename",
                "old_reliability_ranking",
                "timestamp",
            ]:
                """ Ignore these. We don't care for these anymore. """
                pass
            else:
                # pass
                print(f"{activity.activity_identifier}/{activity.id} >> {attr}")
