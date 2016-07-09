'''
TODO: cleanup formset_factory handling.
'''
import urllib.request

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.base import File
from django.forms.models import formset_factory
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.contrib import messages
from wkhtmltopdf import wkhtmltopdf

from landmatrix.storage import data_source_storage
from grid.forms.base_form import BaseForm
from grid.forms.file_field_with_initial import FileFieldWithInitial
from grid.widgets import TitleField, CommentInput

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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
            ("Other (Please specify in comment  field)", _("Other (Please specify in comment  field)")),
        )
    )
    url = forms.URLField(
        required=False, label=_("URL"),
        help_text=_("PDF will be generated automatically, leave empty for file upload")
    )
    file = FileFieldWithInitial(
        required=False, label=_("File"),
        help_text=_("Maximum file size: 2MB")
    )
    file_not_public = forms.BooleanField(
        required=False, label=_("Keep PDF not public")
    )
    publication_title = forms.CharField(
        required=False, label=_("Publication title")
    )
    date = forms.DateField(
        required=False, label=_("Date"), help_text="[YYYY-MM-DD]",
        input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
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
        required=False, label=_("Data source comments"), widget=CommentInput
    )

    def clean_date(self):
        date = self.cleaned_data["date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(
                _("Invalid date. Please enter a date in the format [YYYY-MM-DD]")
            )

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
            #ds_url, ds_file = None, None
            #for t in group["tags"]:
            #    if t["key"] == "url":
            #        ds_url = t["value"]
            #    elif t["key"] == "file":
            #        ds_file = t["value"]
            #if ds_file:
            #    group["tags"].append({
            #            "key": "file",
            #            "value": ds_file,
            #        })
            #if ds_url:
            #    url_slug = "%s.pdf" % re.sub(r"http|https|ftp|www|", "", slugify(ds_url))
            #    if not ds_file or url_slug != ds_file:
            #        # Remove file from group
            #        group["tags"] = filter(lambda o: o["key"] != "file", group["tags"])
            #        # Create file for URL
            #        if not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
            #            try:
            #                # Check if URL changed and no file given
            #                if ds_url.endswith(".pdf"):
            #                    response = urllib.request.urlopen(ds_url)
            #                    default_storage.save("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug), ContentFile(response.read()))
            #                else:
            #                    # Create PDF from URL
            #                    wkhtmltopdf(ds_url, "%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug))
            #                # Set file tag
            #            except:
            #                # skip possible html to pdf conversion errors
            #                if request and not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
            #                    messages.error(request, "Data source <a target='_blank' href='%s'>URL</a> could not be uploaded as a PDF file. Please upload manually." % ds_url)
            #        group["tags"].append({
            #            "key": "file",
            #            "value": url_slug,
            #        })
            #        # always add url, cause there is a problem with storing the file when deal get changed again
            #        #group["tags"].append({
            #        #    "key": "url",
            #        #    "value": ds_url,
            #        #})

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        groups = activity.attributes.filter(
            fk_group__name__startswith=cls.Meta.name).values_list(
            'fk_group__name', flat=True).distinct()

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
    url = form_data['url']
    url_slug = get_url_slug(request, url)

    # TODO: this is a quick and dirty KeyError fix, needs some cleanup
    if not url_slug:
        return form_data

    if 'file' in form_data:
        if url_slug == form_data['file']:
            return form_data
        else:
            # Remove file from group
            del form_data['file']

    # Create file for URL
    if not data_source_storage.exists(url_slug):
        try:
            # Check if URL changed and no file given
            if url.endswith(".pdf"):
                response = urllib.request.urlopen(url)
                data_source_storage.save(url_slug,
                                         ContentFile(response.read()))
            else:
                # Create PDF from URL
                # TODO: fix NameError (uploaded_pdf_path)
                output = wkhtmltopdf(pages=url, output=uploaded_pdf_path)
            form_data['date'] = timezone.now().strftime("%Y-%m-%d")
            form_data['file'] = url_slug
        except Exception as e:
            print(e)
            # skip possible html to pdf conversion errors
            # if request and not default_storage.exists(uploaded_pdf_path):
            error_could_not_upload(request, url, str(e))

    return form_data


def get_url_slug(request, url):
    import re
    from django.template.defaultfilters import slugify

    try:
        urllib.request.urlopen(url)
    except (urllib.error.HTTPError, urllib.error.URLError):
        error_could_not_upload(request, url)
        return None
    except:
        return None

    return "%s.pdf" % re.sub(r"https|http|ftp|www|", "", slugify(url))


def error_could_not_upload(request, url, message=''):
    messages.error(
        request,
        _("Data source <a target='_blank' href='{0}'>URL</a> "
          "could not be uploaded as a PDF file. {1} <br>"
          "Please upload manually.").format(url, message)
    )

