import os.path

from django.core.files.storage import FileSystemStorage
from django.conf import settings


data_source_storage = FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, settings.DATA_SOURCE_DIR),
    base_url=settings.MEDIA_URL + settings.DATA_SOURCE_DIR)
