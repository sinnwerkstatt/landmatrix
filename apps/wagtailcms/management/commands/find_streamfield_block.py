from typing import Any, TypedDict

from django.core.management.base import BaseCommand
from wagtail.blocks import StreamValue, StructValue
from wagtail.blocks.list_block import ListValue  # noqa
from wagtail.fields import StreamField
from wagtail.models import Page

Context = TypedDict("Context", {"page": Page, "path": list[str]})


class Command(BaseCommand):
    help = "Find all usages of a particular streamfield block."

    def add_arguments(self, parser):
        parser.add_argument("block_class", type=str)

    def handle(self, *args, **options):
        block_class = options["block_class"]

        print(f"{'id':>5}", f"{'type':20}", f"{'url':30}", "path")

        for page in Page.objects.all().specific().order_by("id"):

            stream_fields = [
                field
                for field in page._meta.fields  # noqa
                if isinstance(field, StreamField)
            ]

            for field in stream_fields:
                find_block_recursively(
                    getattr(page, field.name),
                    block_class,
                    Context(page=page, path=[field.name]),
                )


def print_info(context: Context):
    page, path = context["page"], context["path"]

    print(
        f"{page.id:05}",
        f"{type(page).__name__:20}",
        f"{page.get_url():30}",
        f"{" -> ".join(path):30}",
    )


def find_block_recursively(value: Any, block_class: str, context: Context):
    page, path = context["page"], context["path"]

    if type(value) is StreamValue:
        # child: StreamValue.StreamChild / Any
        for child in value:
            child_context = Context(page=page, path=[*path, child.block_type])
            child_block_class = type(child.block).__name__

            if block_class == child_block_class:
                print_info(child_context)

            find_block_recursively(child.value, block_class, child_context)

    if type(value) is StructValue:
        declared_blocks = value.block.declared_blocks

        # child: Any
        for key, child in value.items():
            child_context = Context(page=page, path=[*path, key])
            child_block_class = type(declared_blocks[key]).__name__

            if block_class == child_block_class:
                print_info(child_context)

            find_block_recursively(child, block_class, child_context)

    if type(value) is ListValue:
        child_block_class = type(value.list_block.child_block).__name__

        # child: ListValue.ListChild / Any
        for i, child in enumerate(value):
            child_context = Context(page=page, path=[*path, str(i)])

            if block_class == child_block_class:
                print_info(child_context)

            find_block_recursively(child, block_class, child_context)
