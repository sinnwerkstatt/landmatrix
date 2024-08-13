import re

from tqdm import tqdm

from django.core.management import BaseCommand

from apps.landmatrix.models.deal import DealVersion


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

        count = 0
        total = DealVersion.objects.count()
        iterator = DealVersion.objects.iterator()

        print("Iterating DealVersions.")
        for version in tqdm(iterator, total=total):
            updated = fix_text_array_fields(version)

            if updated:
                try:
                    version.save()
                    count += 1
                except Exception as e:
                    print(f"Could not save DealVersion {version}")
                    print(f"Error: {e}")
                    print()

        print(f"Updated {count} DealVersions")
        print("DONE")


def is_non_empty_string(string: str) -> bool:
    return bool(string.strip())


def has_empty_strings(array: list[str]) -> bool:
    return not all(map(is_non_empty_string, array))


def filter_empty_strings(array: list[str]) -> list[str]:
    return list(filter(is_non_empty_string, array))


def fix_text_array_fields(version: DealVersion) -> bool:
    updated = False

    for field_name in ["name_of_indigenous_people", "name_of_community"]:
        field_value = getattr(version, field_name)

        if has_empty_strings(field_value):
            new_field_value = filter_empty_strings(field_value)
            # print(version.id, field_value, new_field_value)
            setattr(version, field_name, new_field_value)
            updated = True

    return updated
