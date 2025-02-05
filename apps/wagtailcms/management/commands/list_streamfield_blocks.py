from collections import Counter
from typing import Any

from django.core.management.base import BaseCommand
from wagtail.blocks import StreamValue, StructValue
from wagtail.blocks.list_block import ListValue  # noqa
from wagtail.fields import StreamField
from wagtail.models import Page


class Command(BaseCommand):
    help = "List streamfield blocks in use."

    def handle(self, *args, **options):

        block_counter = Counter()

        for page in Page.objects.all().specific().order_by("id"):
            # print(f"{page.id:04d}", type(page).__name__, page.get_url())

            stream_fields = [
                field
                for field in page._meta.fields  # noqa
                if isinstance(field, StreamField)
            ]

            for field in stream_fields:
                # print(field.name, type(field).__name__)
                block_counter += get_used_blocks_recursively(getattr(page, field.name))
                # print()

            # print()

        for key, val in block_counter.most_common():
            print(key, val)


def get_used_blocks_recursively(value: Any, level=0):
    # print(4 * level * " " + " -> ", type(value))

    block_counter = Counter()

    if type(value) is StreamValue:
        # child: StreamValue.StreamChild / Any
        for child in value:
            child_block_class = type(child.block).__name__

            block_counter += Counter({child_block_class})
            block_counter += get_used_blocks_recursively(child.value, level + 1)

    if type(value) is StructValue:
        declared_blocks = value.block.declared_blocks

        # child: Any
        for key, child in value.items():
            child_block_class = type(declared_blocks[key]).__name__

            block_counter += Counter({child_block_class})
            block_counter += get_used_blocks_recursively(child, level + 1)

    if type(value) is ListValue:
        child_block_class = type(value.list_block.child_block).__name__

        # child: ListValue.ListChild / Any
        for child in value:
            block_counter += Counter({child_block_class})
            block_counter += get_used_blocks_recursively(child, level + 1)

    return block_counter
