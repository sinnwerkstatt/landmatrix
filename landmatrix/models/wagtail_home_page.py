from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class WagtailHomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel('body', classname="full")]
