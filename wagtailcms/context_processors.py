from wagtailcms.models import WagtailRootPage

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def add_root_page(request):
    return {'wagtail_root_page': WagtailRootPage.objects.first()}