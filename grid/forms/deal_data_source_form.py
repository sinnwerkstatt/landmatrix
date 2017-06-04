'''
TODO: cleanup formset_factory handling.
'''
import re
import http.client
import os

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.base import File
from django.forms.models import formset_factory
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.contrib import messages
from django.conf import settings
from wkhtmltopdf import wkhtmltopdf

from landmatrix.storage import data_source_storage
from grid.forms.base_form import BaseForm
from grid.fields import TitleField, FileFieldWithInitial
from grid.widgets import CommentInput


class DealDataSourceForm(BaseForm):
    form_title = 'Data source'

    tg_data_source = TitleField(
        required=False, label="", initial=_("Data source")
    )
    type = forms.TypedChoiceField(
        required=False, label=_("Data source type"), choices=(
            ("", _("---------")),
            ("Media report", _("Media report")),
            ("Research Paper / Policy Report", _("Research Paper / Policy Report")),
            ("Government sources", _("Government sources")),
            ("Company sources", _("Company sources")),
            ("Contract", _("Contract")),
            ("Contract (contract farming agreement)", _("Contract (contract farming agreement)")),
            ("Personal information", _("Personal information")),
            ("Crowdsourcing", _("Crowdsourcing")),
            ("Other", _("Other (Please specify in comment field)")),
        )
    )
    url = forms.URLField(
        required=False, label=_("URL"),
        help_text=_("PDF will be generated automatically, leave empty for file upload")
    )
    file = FileFieldWithInitial(
        required=False, label=_("File"),
        help_text=_("Maximum file size: 10MB")
    )
    file_not_public = forms.BooleanField(
        required=False, label=_("Keep PDF not public")
    )
    publication_title = forms.CharField(
        required=False, label=_("Publication title")
    )
    date = forms.CharField(
        required=False, label=_("Date"), help_text="[YYYY-MM-DD]",
    #    input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )

    # Optional personal information for Crowdsourcing and Personal information
    name = forms.CharField(required=False, label=_("Name"))
    company = forms.CharField(required=False, label=_("Organisation"))
    email = forms.CharField(required=False, label=_("Email"))
    phone = forms.CharField(required=False, label=_("Phone"))
    includes_in_country_verified_information = forms.BooleanField(
        required=False, label=_("Includes in-country-verified information")
    )
    open_land_contracts_id = forms.CharField(
        required=False, label=_("OpenLandContracts ID")
    )
    tg_data_source_comment = forms.CharField(
        required=False, label=_("Comment on Data source"), widget=CommentInput
    )

    #def clean_date(self):
    #    date = self.cleaned_data["date"]
    #    try:
    #        return date and date.strftime("%Y-%m-%d") or ""
    #    except ValueError:
    #        raise forms.ValidationError(
    #            _("Invalid date. Please enter a date in the format [YYYY-MM-DD]")
    #        )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file and isinstance(file, File):
            n = file.name.split(".")
            # cleanup special charachters in filename
            file.name = "%s.%s" % (slugify(n[0]), n[1]) if len(n)>1 else slugify(n[0])
        return file

    def get_availability_total(self):
        return 4

    def get_fields_display(self):
        if self.initial.get('file_not_public', False):
            self.initial.pop('file')
        return super().get_fields_display()

    #    #next_group_id = next_group.id if next_group else ActivityAttributeGroup.objects.order_by('pk').last().id
    #    #if hasattr(deal.activity, 'history_date'):  # isinstance(deal, DealHistoryItem):
    #    #    deal_date = deal.activity.history_date
    #    #    deal_activity = Activity.objects.get(pk=deal.activity.id).history.as_of(deal_date)
    #    #else:
    #    #    deal_activity = deal.activity
    #    #tags = ActivityAttributeGroup.objects.filter(fk_activity=deal_activity).\
    #    #    filter(pk__gte=group.id).filter(pk__lte=next_group_id).\
    #    #    filter(belongs_to_data_source).values_list('attributes', flat=True)
#
    #    attributes = {}
    #    for tag in tags:
    #        for key in tag.keys():
    #            if key in attributes and attributes[key] != tag[key]:
    #                # raise RuntimeError()
    #                # print(
    #                #     'ALERT: found different values under the same tag group. Deal ID {}, group {}, tags {}'.format(
    #                #         deal.activity.activity_identifier, group.id, str(tags)
    #                #     ))
    #                pass
    #            attributes[key] = tag[key]
#
    #    return attributes


DealDataSourceBaseFormSet = formset_factory(DealDataSourceForm, extra=0)


class AddDealDataSourceFormSet(DealDataSourceBaseFormSet):
    form_title = _('Data sources')
    extra = 1
    max_num = 1

    def get_attributes(self, request=None):
        attributes = []
        for count, form in enumerate(self.forms):
            form_attributes = form.get_attributes(request)

            # FIXME: Move this to DealDataSourceForm.get_attributes
            uploaded = get_file_from_upload(request.FILES, count)
            if uploaded:
                if 'file' in form_attributes:
                    form_attributes['file']['value'] = uploaded
                else:
                    form_attributes['file'] = {'value': uploaded}
            if 'url' in form_attributes and form_attributes['url'] and 'file' not in form_attributes:
                form_attributes = handle_url(form_attributes, request)

            attributes.append(form_attributes)
        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        groups = activity.attributes.filter(
            fk_group__name__startswith=cls.Meta.name).values_list(
            'fk_group__name', flat=True).order_by('fk_group__name').distinct()
        data = []
        for i, group in enumerate(groups):
            form_data = DealDataSourceForm.get_data(activity, group=group)#, prefix='%s-%i' % (cls.Meta.name, i))
            if form_data:
                data.append(form_data)
        return data

    class Meta:
        name = 'data_source'


class ChangeDealDataSourceFormSet(AddDealDataSourceFormSet):
    extra = 0


class PublicViewDealDataSourceForm(DealDataSourceForm):

    class Meta:
        name = 'data_source'
        fields = (
            "tg_data_source", "type", "url", "company", "date"
        )
        readonly_fields = (
            "tg_data_source", "type", "url", "company", "date"
        )


class PublicViewDealDataSourceFormSet(
    formset_factory(PublicViewDealDataSourceForm, formset=AddDealDataSourceFormSet, extra=0)
):
    form_title = _('Data sources')


def get_file_from_upload(files, form_index):
    try:
        key = next(k for k in files.keys() if 'form-{}-file'.format(form_index))
        file = files.getlist(key)[0]
        return data_source_storage.save(file.name, file)
    except (StopIteration, IndexError, AttributeError):
        return None


def handle_url(form_data, request):
    url = form_data['url']['value']
    if not url:
        return
    url_match = re.match('(?P<protocol>.*?:\/\/)?(?P<domain>.*?\..*?)(?P<path>\/.*)?$', url)
    if url_match:
        url_match = url_match.groupdict()
    else:
        raise ValueError(url)
    url_slug = '%s.pdf' % slugify('%s%s' % (url_match['domain'], url_match['path']))

    if 'file' in form_data:
        if url_slug == form_data['file']:
            return form_data
        else:
            # Remove file from group
            del form_data['file']

    # Create file for URL
    if not data_source_storage.exists(url_slug):
        try:
            if 'https' in url_match['protocol']:
                conn = http.client.HTTPSConnection(url_match['domain'])
            else:
                conn = http.client.HTTPConnection(url_match['domain'])
            conn.request('GET', url)
            response = conn.getresponse()

            # PDF URL given?
            if url.endswith(".pdf"):
                # Save to storage
                data_source_storage.save(url_slug,
                                         ContentFile(response.read()))
            else:
                # Save HTML to temp file
                # Create PDF from saved HTML file
                # (WKHTMLTOPDF can handle URLs too, but it does so very badly especially with SSL)
                temp_file = os.path.join(settings.MEDIA_ROOT, settings.DATA_SOURCE_DIR, '%s.html' % url_slug)
                with open(temp_file, 'w') as f:
                    f.write(str(response.read()))
                file_name = os.path.join(settings.MEDIA_ROOT, settings.DATA_SOURCE_DIR, url_slug)
                output = wkhtmltopdf(pages=temp_file, output=file_name)
                os.remove(temp_file)
            form_data['date'] = timezone.now().strftime("%Y-%m-%d")
            form_data['file'] = url_slug
        except Exception as e:
            print(e)
            # skip possible html to pdf conversion errors
            # if request and not default_storage.exists(uploaded_pdf_path):
            messages.error(
                request,
                _("Data source <a target='_blank' href='{0}'>URL</a> "
                  "could not be downloaded as a PDF file."
                  "Please upload manually.").format(url)
            )
    else:
        form_data['file'] = url_slug

    return form_data


