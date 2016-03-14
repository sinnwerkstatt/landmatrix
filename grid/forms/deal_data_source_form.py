from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.deal_history import DealHistoryItem

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.base_form import BaseForm
from grid.forms.file_field_with_initial import FileFieldWithInitial
from grid.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import File
from django.forms.models import formset_factory
from django.template.defaultfilters import slugify
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib import messages

from wkhtmltopdf import wkhtmltopdf

import urllib.request

import os
import re


class DealDataSourceForm(BaseForm):

    DEBUG = False
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

    @classmethod
    def get_data(cls, deal, taggroup, next_taggroup):
        from django.db.models import Q
        belongs_to_data_source = Q(attributes__contains=['file']) | \
                                 Q(attributes__contains=['url']) | \
                                 Q(attributes__contains=['type']) | \
                                 Q(name__icontains='data_source')

        next_taggroup_id = next_taggroup.id if next_taggroup else ActivityAttributeGroup.objects.order_by('pk').last().id

        if hasattr(deal.activity, 'history_date'):  # isinstance(deal, DealHistoryItem):
            deal_date = deal.activity.history_date
            deal_activity = Activity.objects.get(pk=deal.activity.id).history.as_of(deal_date)
        else:
            deal_activity = deal.activity

        tags = ActivityAttributeGroup.objects.filter(fk_activity=deal_activity).\
            filter(pk__gte=taggroup.id).filter(pk__lte=next_taggroup_id).\
            filter(belongs_to_data_source).values_list('attributes', flat=True)

        attributes = {}
        for tag in tags:
            for key in tag.keys():
                if key in attributes and attributes[key] != tag[key]:
                    # raise RuntimeError()
                    print(
                        'ALERT: found different values under the same tag group. Deal ID {}, taggroup {}, tags {}'.format(
                            deal.activity.activity_identifier, taggroup.id, str(tags)
                        ))
                attributes[key] = tag[key]

        return attributes


DealDataSourceBaseFormSet = formset_factory(DealDataSourceForm, extra=0)


class AddDealDataSourceFormSet(DealDataSourceBaseFormSet):

    form_title = _('Data sources')
    extra = 1

    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
                ds_url, ds_file = None, None
                for t in taggroup["tags"]:
                    if t["key"] == "url":
                        ds_url = t["value"]
                    elif t["key"] == "file":
                        ds_file = t["value"]
                if ds_file:
                    taggroup["tags"].append({
                            "key": "file",
                            "value": ds_file,
                        })
                if ds_url:
                    url_slug = "%s.pdf" % re.sub(r"http|https|ftp|www|", "", slugify(ds_url))
                    if not ds_file or url_slug != ds_file:
                        # Remove file from taggroup
                        taggroup["tags"] = filter(lambda o: o["key"] != "file", taggroup["tags"])
                        # Create file for URL
                        if not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                            try:
                                # Check if URL changed and no file given
                                if ds_url.endswith(".pdf"):
                                    response = urllib.request.urlopen(ds_url)
                                    default_storage.save("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug), ContentFile(response.read()))
                                else:
                                    # Create PDF from URL
                                    wkhtmltopdf(ds_url, "%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug))
                                # Set file tag
                            except:
                                # skip possible html to pdf conversion errors
                                if request and not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                                    messages.error(request, "Data source <a target='_blank' href='%s'>URL</a> could not be uploaded as a PDF file. Please upload manually." % ds_url)
                        taggroup["tags"].append({
                            "key": "file",
                            "value": url_slug,
                        })
                        # always add url, cause there is a problem with storing the file when deal get changed again
                        #taggroup["tags"].append({
                        #    "key": "url",
                        #    "value": ds_url,
                        #})
        return ds_taggroups

    @classmethod
    def get_data(cls, deal):
        from django.db.models import Q
        belongs_to_data_source = Q(attributes__contains=['file']) | \
                                 Q(attributes__contains=['url']) | \
                                 Q(attributes__contains=['type']) | \
                                 Q(name__icontains='data_source')
        if not deal:
            return {}

        taggroups = deal.attribute_groups().filter(belongs_to_data_source).order_by('name')

        data = {
            'form-TOTAL_FORMS': len(taggroups),
            'form-INITIAL_FORMS': len(taggroups),
            'form-MAX_NUM_FORMS': 1000
        }
        for i, taggroup in enumerate(taggroups):
            form_data = DealDataSourceForm.get_data(deal, taggroup, taggroups[i+1] if i < len(taggroups)-1 else None)
            # print('AddDealDataSourceFormSet form', i, ':    ', form_data)
            data[i] = form_data
        return data


class ChangeDealDataSourceFormSet(AddDealDataSourceFormSet):

    form_title = _('Data sources')

    extra = 0


class PublicViewDealDataSourceForm(DealDataSourceForm):

    class Meta:
        fields = (
            "tg_data_source", "type", "url", "company", "date"
        )
        readonly_fields = (
            "tg_data_source", "type", "url", "company", "date"
        )

    @classmethod
    def get_data(cls, deal):
        taggroups = deal.attribute_groups().filter(name__contains='data_source').order_by('name')
        print('PublicViewDealDataSourceForm: taggroups    ', taggroups)
        data = {}
        for i, taggroup in enumerate(taggroups):
            data[i] = DealDataSourceForm.get_data(deal, taggroup=taggroup)
        return data


class PublicViewDealDataSourceFormSet(
    formset_factory(PublicViewDealDataSourceForm, formset=AddDealDataSourceFormSet, extra=0)
):

    form_title = _('Data sources')



