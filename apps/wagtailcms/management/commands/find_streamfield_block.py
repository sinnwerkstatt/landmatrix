from django.core.management.base import BaseCommand
from wagtail.models import Page

SF_CLASS_NAMES = [
    "StreamField",
    "TranslationStreamField",
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("blocktype", type=str)

    def handle(self, *args, **options):
        blocktype = options["blocktype"]
        for page in Page.objects.all().specific():
            for field in page._meta.fields:
                if field.__class__.__name__ not in SF_CLASS_NAMES:
                    continue
                sfield = getattr(page, field.name)
                if f"'type': '{blocktype}'" in str(sfield.raw_data):
                    print(page, page.get_url())
