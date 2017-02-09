from wagtailcms.models import WagtailRootPage
from django.conf import settings



def add_root_page(request):
    return {'wagtail_root_page': WagtailRootPage.objects.first()}

def add_data_source_dir(request):
    return {'DATA_SOURCE_DIR': settings.DATA_SOURCE_DIR}