from tqdm import tqdm

from django.core.management import BaseCommand
from django.db.models import QuerySet

from apps.accounts.models import User

from ...models.deal import DealOld, DealVersionOld
from ...models.investor import InvestorOld, InvestorVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Fix created_by object field."""

        for model in [DealOld, InvestorOld]:
            print(f"Fixing {model.__name__} objects...")

            fixed_obj_ids: list[int] = []
            for obj in tqdm(
                model.objects.iterator(),
                total=model.objects.count(),
            ):
                fixed = fix_creator(obj)

                if fixed:
                    fixed_obj_ids.append(obj.id)

            print("Fixed object ids:", {*fixed_obj_ids})


def fix_creator(obj: DealOld | InvestorOld) -> bool:
    assert obj.versions.count() > 0

    creator: User | None = obj.versions.last().created_by
    fixed = False

    if obj.created_by != creator:
        obj.created_by = creator
        obj.save()
        fixed = True

    versions_qs: QuerySet[DealVersionOld | InvestorVersion] = obj.versions.all()

    for version in versions_qs:
        serialized_creator = creator.id if creator else None

        if version.serialized_data["created_by"] != serialized_creator:
            version.serialized_data["created_by"] = serialized_creator
            version.save()
            fixed = True

    return fixed
