from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import URLBlock

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


CONTENT_BLOCKS = [
    ('heading', blocks.CharBlock(classname="full title", icon="title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock(icon="image")),
    ('media', EmbedBlock(icon="media")),
    ('link', URLBlock(icon="link")),
]


class ColumnsBlock(StructBlock):

    left_column = blocks.StreamBlock(CONTENT_BLOCKS)
    right_column = blocks.StreamBlock(CONTENT_BLOCKS, form_classname='pull-right')

    def get_context(self, value):
        context = super().get_context(value)
        context['left_column'] = value.get('left_column')
        context['right_column'] = value.get('right_column')
        return context

    class Meta:
        icon = 'fa fa-columns'
        label = 'Columns 1-1'
        template = None


class Columns1To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:1'
        template = 'widgets/columns-1-1.html'


class Columns2To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 2:1'
        template = 'widgets/columns-2-1.html'


class Columns1To2Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:2'
        template = 'widgets/columns-1-2.html'


class WagtailRootPage(Page):
    body = StreamField(
        [
            ('heading', blocks.CharBlock(classname="full title", icon="title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock(icon="image")),
            ('media', EmbedBlock(icon="media")),
            ('link', URLBlock(icon="link")),
            ('columns_1_1', Columns1To1Block()),
            ('columns_2_1', Columns2To1Block()),
            ('columns_1_2', Columns1To2Block())
        ]
    )
    footer_column_1 = RichTextField(blank=True)
    footer_column_2 = RichTextField(blank=True)
    footer_column_3 = RichTextField(blank=True)
    footer_column_4 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('footer_column_1'),
        FieldPanel('footer_column_2'),
        FieldPanel('footer_column_3'),
        FieldPanel('footer_column_4')
    ]


class WagtailPage(Page):
    body = StreamField(
        [
            ('heading', blocks.CharBlock(classname="full title", icon="title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock(icon="image")),
            ('media', EmbedBlock(icon="media")),
            ('link', URLBlock(icon="link")),
            ('columns_1_1', Columns1To1Block()),
            ('columns_2_1', Columns2To1Block()),
            ('columns_1_2', Columns1To2Block())
        ]
    )
    content_panels = Page.content_panels + [StreamFieldPanel('body')]
