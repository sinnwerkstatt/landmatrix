__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.core.files.uploadedfile import UploadedFile, SimpleUploadedFile
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import os

class FileInputWithInitial(forms.ClearableFileInput):

    NUM_DISPLAYED_CHARS = 40
    # UPLOAD_BASE_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads')
    UPLOAD_BASE_DIR = '/media/uploads'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        output = []
        if value:
            value = isinstance(value, UploadedFile) and value.name or value
            output.extend([
                "<dl>",
                "<dt>{}:</dt>".format(_("Saved file")),
                "<dd>",
                '<a href="{}/{}" target="_blank">{}...</a>'.format(
                    self.UPLOAD_BASE_DIR, value, value[:self.NUM_DISPLAYED_CHARS]
                ),
                '<input type="hidden" name="{}" value="{}">'.format(name, value),
                "</dd>",
                "</dl>"
            ])
        output.append(super().render("%s-new" % name, value, attrs))
        return "\n".join(output)

    def value_from_datadict(self, data, files, name):
        new_file = files.get("%s-new" % name)
        if new_file:
            return new_file
        value = data.get(name)
        if value:
            return SimpleUploadedFile(name=value, content=b'test')
        return ""


class FileFieldWithInitial(forms.FileField):
    widget = FileInputWithInitial
    show_hidden_initial = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
