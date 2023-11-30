import json

from django.core.management.base import BaseCommand
from wagtail.models import Site

from apps.wagtailcms.models import WagtailRootPage


class Command(BaseCommand):
    help = "Build new homepage according to screen design (2023)."

    def handle(self, *args, **kwargs):
        root_page: WagtailRootPage = Site.objects.get(
            is_default_site=True
        ).root_page.specific

        root_page.body_en = json.dumps(BODY)
        root_page.body_fr = None
        root_page.body_es = None
        root_page.body_ru = None

        root_page.save()


BODY = [
    {
        "type": "image_text_block",
        "value": {
            "title": "",
            "subtitle": "Promoting transparency and accountability in land acquisitions",
            "text": '<p data-block-key="7ziwi">The Land Matrix is an independent land monitoring initiative that promotes transparency and accountability in decisions over large-scale land acquisitions (LSLAs) in low- and middle-income countries by capturing and sharing data about these deals.</p>',
            "link": {"page": None, "external_url": "", "text": "Report a deal"},
            "image": 558,
            "bg_color": "orange",
        },
        "id": "c7e7f0be-b6f2-4f61-8a42-78493f6c93a1",
    },
    {
        "type": "dealcount",
        "value": {"text": "It's a big deal"},
        "id": "b1a13914-80b1-4d65-b783-98957a0985df",
    },
    {
        "type": "data_teaser",
        "value": {
            "title": "Our data",
            "subtitle": "Discover and download our  interactive data through…",
            "cards": [
                {
                    "type": "item",
                    "value": {
                        "title": "Maps",
                        "teaser": "Discover and download our interactive data through…",
                        "link": {
                            "page": None,
                            "external_url": "",
                            "text": "Go to maps >>",
                        },
                    },
                    "id": "d276b06e-1a79-4d20-82f7-ff8dd6149399",
                },
                {
                    "type": "item",
                    "value": {
                        "title": "Charts",
                        "teaser": "Use a wide selection of charts to illustrate information about deals.",
                        "link": {
                            "page": None,
                            "external_url": "",
                            "text": "Go to charts >>",
                        },
                    },
                    "id": "9daf91f7-cdaa-4ff1-adb3-c50efd515113",
                },
                {
                    "type": "item",
                    "value": {
                        "title": "Tables",
                        "teaser": "Filter the dataset to find information according to deals or investors.",
                        "link": {
                            "page": None,
                            "external_url": "",
                            "text": "Go to tables >>",
                        },
                    },
                    "id": "793d193d-a0cc-497e-84e2-b798f3d5f49a",
                },
            ],
        },
        "id": "6833bc5a-14ae-498d-95a1-49965ed434a5",
    },
    {
        "type": "latest_resources",
        "value": {
            "title": "Announcements",
            "subtitle": "Latest resources",
            "article_highlight": 22,
        },
        "id": "d045bb62-bd0c-4e4d-9e95-81f580de7fc0",
    },
    {
        "type": "image_text_block",
        "value": {
            "title": "Contribute",
            "subtitle": "Report a deal or suggest changes",
            "text": '<p data-block-key="ozzn3">Do you have information about land deals in your country that we can add to our database? Can you confirm or update information we already have? You can help us make the Land Matrix more accurate and comprehensive by adding a deal, providing feedback on existing data, or contacting us with any other queries or suggestions.</p>',
            "link": {"page": None, "external_url": "", "text": "Report now"},
            "image": 559,
            "bg_color": "white",
        },
        "id": "19c4d9a5-7141-4c64-aace-85d7b9a7da5b",
    },
    {"type": "partners", "value": {}, "id": "1581c917-d8e1-46bd-ba14-e4118ea5881b"},
]
