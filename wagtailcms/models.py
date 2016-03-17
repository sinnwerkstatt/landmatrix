from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import Block, URLBlock, RawHTMLBlock, StreamBlock

from django.utils.html import format_html, format_html_join, force_text
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

#FIXME: Move blocks to blocks.py
CONTENT_BLOCKS = [
    ('heading', blocks.CharBlock(classname="full title", icon="title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
    ('media', EmbedBlock(icon="media")),
    ('link', URLBlock(icon="link")),
    ('html', RawHTMLBlock(icon="code")),
]

# Overwrite Stream block to disable wrapping DIVs
class NoWrapsStreamBlock(StreamBlock):
    def render_basic(self, value):
        return format_html_join(
            '\n', '<div class="{1}">{0}</div>',
            [(force_text(child), child.block_type != 'full_width_container' and 'block-%s block'%child.block_type or '') for child in value]
        )
        #return format_html_join(
        #    '\n', '{0}',
        #    [(force_text(child), child.block_type) for child in value]
        #)

class NoWrapsStreamField(StreamField):
    def __init__(self, block_types, **kwargs):
        super(NoWrapsStreamField, self).__init__(block_types, **kwargs)
        if isinstance(block_types, Block):
            self.stream_block = block_types
        elif isinstance(block_types, type):
            self.stream_block = block_types()
        else:
            self.stream_block = NoWrapsStreamBlock(block_types)

class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context

class SectionDivider(StructBlock):
    class Meta:
        icon = 'image'
        template = 'widgets/divider.html'

class LinkedImageBlock(StructBlock):
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['href'] = value.url
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context

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

class SliderBlock(StructBlock):
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value):
        context = super().get_context(value)
        images_data = value.get('images')
        images = []
        if images_data:
            for image in images_data:
                rendition = image.get('image').get_rendition('max-1200x1200')
                url = rendition.url
                name = image.get('image').title
                image_context = {'url': url, 'name': name, 'href': image.get('url')}
                images.append(image_context)
        context['images'] = images
        return context

    class Meta:
        icon = 'fa fa-picture-o'
        label = 'Slider'
        template = 'widgets/slider.html'

class GalleryBlock(StructBlock):
    columns = blocks.ChoiceBlock(choices=[
        (1, '1 column'),
        (2, '2 columns'),
        (3, '3 columns'),
        (4, '4 columns'),
        (5, '5 columns'),
        (6, '6 columns'),
    ], icon='fa fa-columns')
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value):
        context = super().get_context(value)
        columns_data = value.get('columns')
        if columns_data and columns_data.isdigit():
            context['columns'] = int(columns_data)
        images_data = value.get('images')
        images = []
        if images_data:
            for image in images_data:
                rendition = image.get('image').get_rendition('max-1200x1200')
                url = rendition.url
                name = image.get('image').title
                image_context = {'url': url, 'name': name, 'href': image.get('url')}
                images.append(image_context)
        context['images'] = images
        return context

    class Meta:
        icon = 'fa fa-picture-o'
        label = 'Gallery'
        template = 'widgets/gallery.html'

class FullWidthContainerBlock(StructBlock):
    color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('lightgrey', 'Light grey'),
        ('darkgrey', 'Dark grey')
    ], default='white')
    content = NoWrapsStreamBlock(CONTENT_BLOCKS, form_classname='pull-right')

    def get_context(self, value):
        context = super().get_context(value)
        context['content'] = value.get('content')
        context['color'] = value.get('color')
        return context

    class Meta:
        icon = 'fa fa-arrows-h'
        label = 'Full width container'
        template = 'widgets/full-width-container.html'

CONTENT_BLOCKS = CONTENT_BLOCKS + [
    ('full_width_container', FullWidthContainerBlock(form_classname='')),
    ('section_divider', SectionDivider()),
    ('gallery', GalleryBlock()),
    ('slider', SliderBlock()),
]

class WagtailRootPage(Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + [
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
    body = NoWrapsStreamField(CONTENT_BLOCKS + [
            ('columns_1_1', Columns1To1Block()),
            ('columns_2_1', Columns2To1Block()),
            ('columns_1_2', Columns1To2Block())
        ]
    )
    content_panels = Page.content_panels + [StreamFieldPanel('body')]

#FIXME: Move hooks to wagtail_hooks.py
@hooks.register('insert_editor_js')
def editor_js():
  return format_html(
    """
    <script>
      registerHalloPlugin('hallojustify');
    </script>
    """
  )

@hooks.register('insert_editor_css')
def editor_css():
    # Add extra CSS files to the admin like font-awesome
    css_files = [
        'vendor/font-awesome/css/font-awesome.min.css',
        'css/wagtail-font-awesome.css'
    ]

    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files))

    return css_includes

@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'h2': attribute_rule({'style': True}),
        'h3': attribute_rule({'style': True}),
        'h4': attribute_rule({'style': True}),
        'h5': attribute_rule({'style': True}),
        'p': attribute_rule({'style': True}),
    }