from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Count

from apps.landmatrix.management.helpers import db_require_confirmation
from apps.landmatrix.models.investor import Involvement


class Command(BaseCommand):
    help = "Find and fix involvement duplicates."

    @db_require_confirmation
    def handle(self, *args, **options):
        qs_duplicates = (
            Involvement.objects.values("child_investor", "parent_investor")
            .order_by("parent_investor_id", "child_investor_id")
            .annotate(child_parent_count=Count("id"))
            .filter(child_parent_count__gt=1)
        )

        print()
        print(f"Found {len(qs_duplicates)} duplicate involvements:")
        print(f'{"child":>8}', f'{"parent":>8}', f'{"n":>2}')

        with transaction.atomic():
            for duplicate in qs_duplicates:
                print(
                    f"{duplicate['child_investor']:8d}",
                    f"{duplicate['parent_investor']:8d}",
                    f"{duplicate['child_parent_count']:2d}",
                    end=" ",
                )

                qs_involvements = Involvement.objects.filter(
                    child_investor=duplicate["child_investor"],
                    parent_investor=duplicate["parent_investor"],
                ).order_by("id")

                qs_ids = qs_involvements.values_list("id", flat=True)
                qs_values = qs_involvements.values(
                    # "id",
                    "role",
                    "investment_type",
                    "percentage",
                    "loans_amount",
                    "loans_currency",
                    "loans_date",
                    "parent_relation",
                    "comment",
                )

                if qs_values.distinct().count() > 1:
                    # print distinct involvement ids
                    qs_distinct_ids = qs_values.distinct().values_list("id", flat=True)
                    print("CANNOT FIX", list(qs_distinct_ids))
                else:
                    # delete all but one involvement
                    qs_involvements.filter(id__in=qs_ids[1:]).delete()
                    print("FIXED")

        print("DONE")
