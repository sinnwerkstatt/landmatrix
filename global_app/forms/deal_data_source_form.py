__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.base_form import BaseForm
from global_app.forms.file_field_with_initial import FileFieldWithInitial
from global_app.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import File
from django.template.defaultfilters import slugify


class DealDataSourceForm(BaseForm):

    tg_data_source = TitleField(required=False, label="", initial=_("Data source"))
    type = forms.TypedChoiceField(required=False, label=_("Data source type"), choices=(
        (10, _("Media report")),
        (20, _("Research Paper / Policy Report")),
        (30, _("Government sources")),
        (40, _("Company sources")),
        (50, _("Contract")),
        (60, _("Personal information")),
        (70, _("Crowdsourcing")),
        (80, _("Other (Please specify in comment  field)")),
    ), coerce=int)
    url = forms.URLField(required=False, label=_("New URL"), help_text=_("PDF will be generated automatically, leave empty for file upload"))
    file = FileFieldWithInitial(required=False, label=_("New file"))
    date = forms.DateField(required=False, label=_("Date"), help_text="[dd:mm:yyyy]", input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"])
    # Optional personal information for Crowdsourcing and Personal information
    name = forms.CharField(required=False, label=_("Name"))
    company = forms.CharField(required=False, label=_("Organisation"))
    email = forms.CharField(required=False, label=_("Email"))
    phone = forms.CharField(required=False, label=_("Phone"))
    includes_in_country_verified_information = forms.BooleanField(required=False, label=_("Includes in-country-verified information"))
    tg_data_source_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def clean_date(self):
        date = self.cleaned_data["date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(_("Invalid date. Please enter a date in the format [dd:mm:yyyy]"))

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file and isinstance(file, File):
            n = file.name.split(".")
            # cleanup special charachters in filename
            file.name = "%s.%s" % (slugify(n[0]), n[1]) if len(n)>1 else slugify(n[0])
        return file

    def get_availability_total(self):
        return 4

    def __init__(self, *args, **kwargs):
        super(DealDataSourceForm, self).__init__(*args, **kwargs)
