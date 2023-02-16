import json
from collections import defaultdict

from tqdm import tqdm

from django.core.management import BaseCommand

from ...models.deal import DealVersion

DEAL_FIELDS_TO_BE_DELETED = [
    "confidential_reason",
    "prai_applied",
    "prai_applied_comment",
    "vggt_applied",
    "vggt_applied_comment",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Delete old deal fields from serialized data"""
        counts = defaultdict(int)

        print("Iterating DealVersions")
        for v in tqdm(
            DealVersion.objects.iterator(),
            total=DealVersion.objects.count(),
        ):
            for field_name in DEAL_FIELDS_TO_BE_DELETED:
                try:
                    del v.serialized_data[field_name]
                    v.save()
                    counts[field_name] += 1
                except KeyError:
                    continue

        print("deleted", json.dumps(counts, indent=2))
