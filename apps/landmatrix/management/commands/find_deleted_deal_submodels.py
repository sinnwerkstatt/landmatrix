import sys
from dataclasses import dataclass
from datetime import datetime

import pytz
import termtables as tt
from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import Deal


@dataclass
class DataSource:
    id: int
    type: str
    url: str
    file: str
    file_not_public: str
    publication_title: str
    date: str
    name: str
    company: str
    email: str
    phone: str
    includes_in_country_verified_information: str
    open_land_contracts_id: str
    comment: str
    old_group_id: int

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.url == other.url
            and self.old_group_id == other.old_group_id
        )

    def samebutgroup(self, other):
        return self.type == other.type and self.url == other.url

    def print(self):
        data = [
            ["id:", self.id],
            ["type:", self.type],
            ["url:", self.url],
            ["file:", self.file],
            ["file_not_public:", self.file_not_public],
            ["publication_title:", self.publication_title],
            ["date:", self.date],
            ["name:", self.name],
            ["company:", self.company],
            ["email:", self.email],
            ["phone:", self.phone],
            [
                "includes_verified:",
                self.includes_in_country_verified_information,
            ],
            [
                "open_land_contracts_id:",
                self.open_land_contracts_id,
            ],
            # ["comment:", a.comment, b.comment],
            ["old_group_id:", self.old_group_id],
        ]
        tt.print(
            data,
            padding=(0, 0),
            # alignment="lcr",
        )

    @staticmethod
    def printtwo(a: "DataSource", b: "DataSource"):
        data = [
            ["id:", a.id, b.id],
            ["type:", a.type, b.type],
            ["url:", a.url, b.url],
            ["file:", a.file, b.file],
            ["file_not_public:", a.file_not_public, b.file_not_public],
            ["publication_title:", a.publication_title, b.publication_title],
            ["date:", a.date, b.date],
            ["name:", a.name, b.name],
            ["company:", a.company, b.company],
            ["email:", a.email, b.email],
            ["phone:", a.phone, b.phone],
            [
                "includes_verified:",
                a.includes_in_country_verified_information,
                b.includes_in_country_verified_information,
            ],
            [
                "open_land_contracts_id:",
                a.open_land_contracts_id,
                b.open_land_contracts_id,
            ],
            # ["comment:", a.comment, b.comment],
            ["old_group_id:", a.old_group_id, b.old_group_id],
        ]
        tt.print(
            data,
            padding=(0, 0),
            # alignment="lcr",
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        global_count = 0
        global_multi_delete = 0
        deals = Deal.objects.active().order_by("id")
        deal_count = deals.count()

        cutoff = datetime(2018, 10, 1, tzinfo=pytz.UTC)
        for i, deal in enumerate(deals):
            pre_dses = []
            has_problems = False
            deletion_events = 0

            offset = 0
            for dv in deal.versions.all().order_by("pk"):
                dses = dv.serialized_data["datasources"]

                if dv.created_at < cutoff:
                    pre_dses = dses
                    continue

                if len(pre_dses) > len(dses):
                    # for i, ds in enumerate(dses):
                    #     dsnew = DataSource(**ds)
                    #     dsold = DataSource(**pre_dses[i])
                    #     if dsold == dsnew:
                    #         assert dsold.file == dsnew.file
                    #     if dsold != dsnew:
                    #         dsold2 = DataSource(**pre_dses[i + 1])
                    #         if dsnew.file == dsold.file:
                    #             dsnew.file = dsold2.file
                    #             # dsnew.old_group_id = dsold2.old_group_id
                    #         # print(dv)
                    #         DataSource.printtwo(dsold, dsold2)
                    #         dsnew.print()
                    #         # DataSource.printtwo(dsnew, dsold)

                    deletion_events += 1
                    # print(dv)
                    has_problems = True
                    # print([DataSource(**ds) for ds in dses])
                    continue
                    # print(pre_dses, dses)
                    # print(list([ds["id"], ds["url"], ds["file"]] for ds in dses))
                pre_dses = dses

            if has_problems:
                print(
                    f'{deal.id};{deal.country.region.name};{deal.country.name};=HYPERLINK("https://dev.landmatrix.org/deal/{deal.id}/datasources_table/")'
                )
                global_count += 1
            if deletion_events > 1:
                global_multi_delete += 1
                # print(f"{deletion_events=}")
            # print(f"\r{i} / {deal_count}", end="")
        print("")
        print(global_count)
        print(f"{global_multi_delete=}")
