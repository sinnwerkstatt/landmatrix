'''
TODO: move to widgets/fields
'''
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

from landmatrix.storage import data_source_storage


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FileInputWithInitial(forms.ClearableFileInput):
    displayed_chars = 40
    existing_file_template = '<a class="input-group-addon" href="{url}" target="_blank" title="' + str(_('Current file')) \
        + ' class="toggle-tooltip"><i class="fa fa-file-pdf-o"></i></a>'
    new_upload_template = "{}-new"

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        output = ""

        if value:
            if self.is_initial(value):
                # previously uploaded file
                value_name = str(value.name)
                value_url = value.url
            else:
                value_name = str(value)
                value_url = data_source_storage.url(value)

            if len(value_name) > self.displayed_chars:
                display_name = value_name[:self.displayed_chars] + '...'
            else:
                display_name = value_name

            output += self.existing_file_template.format(label=_("Saved file"),
                                                         url=value_url,
                                                         name=display_name)


        file_input = super().render(self.new_upload_template.format(name),
                                    None, attrs)
        output += file_input

        return output

    def value_from_datadict(self, data, files, name):
        new_file_name = self.new_upload_template.format(name)

        try:
            value = files[new_file_name]
        except KeyError:
            value = None

        return value


class FileFieldWithInitial(forms.FileField):
    widget = FileInputWithInitial
    show_hidden_initial = True

    def validate(self, value):
        '''
        For new uploads only, check that size is less than our max.

        This doesn't prevent DOS attacks (for that we'd need to limit the
        webserver) but it does let us give the user a nice error message.
        '''
        if value and value._size > settings.DATA_SOURCE_MAX_UPLOAD_SIZE:
            raise ValidationError(_("Uploaded files must be less than 10MB."))
