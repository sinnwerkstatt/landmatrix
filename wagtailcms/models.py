from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class WagtailRootPage(Page):
    body = RichTextField(blank=True)
    footer_column_1 = RichTextField(blank=True)
    footer_column_2 = RichTextField(blank=True)
    footer_column_3 = RichTextField(blank=True)
    footer_column_4 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('footer_column_1'),
        FieldPanel('footer_column_2'),
        FieldPanel('footer_column_3'),
        FieldPanel('footer_column_4')
    ]


class WagtailPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('body', classname="full")]
