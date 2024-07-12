import re

from tqdm import tqdm

from django.core.management import BaseCommand

from apps.landmatrix.models.deal import DealOld, DealVersionOld

JSON_fields = [
    "contract_size",
    "production_size",
    "intention_of_investment",
    "negotiation_status",
    "implementation_status",
    "on_the_lease",
    "off_the_lease",
    "total_jobs_current",
    "foreign_jobs_current",
    "domestic_jobs_current",
    "involved_actors",
    "crops",
    "animals",
    "mineral_resources",
    "contract_farming_crops",
    "contract_farming_animals",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        confirm = input(
            "***** ATTENTION ***** \n"
            "This command potentially manipulates DB. \n"
            "Make sure DB connection is configured correctly in .env. \n"
            "Confirm to continue (y/N): "
        )

        if not confirm or not re.match("^y(es)?$", confirm, re.I):
            print("Aborting")
            return

        print("Iterating Deals.")
        # Todo?!
        n_deals = DealOld.objects.count()
        deal_iterator = DealOld.objects.iterator()
        for _ in tqdm(range(n_deals)):
            deal = next(deal_iterator)
            forward_deal(deal)
            deal.save()

        print("Iterating DealVersions.")
        n_versions = DealVersionOld.objects.count()
        version_iterator = DealVersionOld.objects.iterator()
        for _ in tqdm(range(n_versions)):
            version = next(version_iterator)
            forward_version(version)
            version.save()


def is_empty(x):
    return type(x) is list and len(x) == 0


def forward_deal(deal):
    for field_name in JSON_fields:
        set_model_field(deal, field_name, is_empty, None)


def forward_version(version):
    data = version.serialized_data

    for field_name in JSON_fields:
        set_dict_field(data, field_name, is_empty, None)


def set_model_field(obj, field_name, test_fn, new_value):
    if hasattr(obj, field_name):
        value = getattr(obj, field_name)

        if test_fn(value):
            setattr(obj, field_name, new_value)
    else:
        print(f"Unknown field name {field_name} on obj {obj}")


def set_dict_field(obj: dict, field_name, test_fn, new_value):
    if test_fn(obj[field_name]):
        obj[field_name] = new_value
