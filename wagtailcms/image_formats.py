# image_formats.py
from wagtail.images.formats import Format, unregister_image_format, register_image_format

unregister_image_format('fullwidth')
register_image_format(Format('fullwidth', 'Fullwidth', 'richtext-image fullwidth', 'max-1200x1200'))