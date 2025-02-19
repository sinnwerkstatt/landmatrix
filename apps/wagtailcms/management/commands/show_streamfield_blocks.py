from django.core.management.base import BaseCommand
from wagtail.blocks import (
    Block,
    FieldBlock,
    ListBlock,
    StaticBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.fields import StreamField
from wagtail.models import Page, get_page_models


class Command(BaseCommand):
    help = "Print streamfield names and structures for all page models."

    def handle(self, *args, **options):
        page_model: Page
        for page_model in get_page_models():
            print(page_model.__name__)

            stream_fields = [
                field for field in page_model._meta.fields if type(field) is StreamField
            ]

            field: StreamField
            for field in stream_fields:
                print(" -> ", field.name)

                blocks = field.stream_block.sorted_child_blocks()

                # grouped by Block.Meta group property:
                # blocks = field.stream_block.grouped_child_blocks()

                for block in blocks:
                    print_blocks_recursively(block)

            print()


def print_blocks_recursively(block: Block, level=1):
    # assert isinstance(block, Block)

    print(4 * level * " " + " -> ", block.name, type(block).__name__)

    # Could be implemented using python 3.10 structural pattern matching, see:
    # https://docs.python.org/3/whatsnew/3.10.html#guard
    if isinstance(block, FieldBlock | StaticBlock):
        ...

    if isinstance(block, ListBlock):
        print_blocks_recursively(block.child_block, level + 1)

    if isinstance(block, StructBlock):
        # child_blocks: OrderedDict
        for child_block in block.child_blocks.values():
            print_blocks_recursively(child_block, level + 1)

    if isinstance(block, StreamBlock):
        for child_block in block.sorted_child_blocks():
            print_blocks_recursively(child_block, level + 1)
