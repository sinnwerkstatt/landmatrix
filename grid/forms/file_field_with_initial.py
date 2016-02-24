__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.core.files.uploadedfile import UploadedFile, SimpleUploadedFile
from django.utils.translation import ugettext_lazy as _

class FileInputWithInitial(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super(FileInputWithInitial, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        output = []
        if value:
            value = isinstance(value, UploadedFile) and value.name or value
            output.append("<dl>")
            output.append("<dt>%s:</dt>" % str(_("Saved file")))
            output.append("<dd>")
            output.append('<a href="/media/uploads/%s" target="_blank"> %s</a>' % (value, value[:25]))
            output.append('<input type="hidden" name="%s" value="%s">' % (name, value))
            output.append("</dd>")
            output.append("</dl>")
        output.append(super(FileInputWithInitial, self).render("%s-new"%name, value, attrs))
        return "\n".join(output)

    def value_from_datadict(self, data, files, name):
        # New file uploaded?
        new_file = files.get("%s-new"%name)
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
        #self.widget = FileInputWithInitial()
        super(FileFieldWithInitial, self).__init__(*args, **kwargs)
