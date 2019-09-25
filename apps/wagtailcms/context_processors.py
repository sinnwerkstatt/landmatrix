from django.conf import settings


# pylint: disable=unused-argument
def add_data_source_dir(request):
    return {"DATA_SOURCE_DIR": settings.DATA_SOURCE_DIR}
