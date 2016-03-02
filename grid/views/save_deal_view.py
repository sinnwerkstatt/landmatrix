from grid.forms.add_deal_employment_form import AddDealEmploymentForm
from grid.forms.add_deal_general_form import AddDealGeneralForm
from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from grid.forms.deal_data_source_form import AddDealDataSourceFormSet, DealDataSourceForm
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_produce_info_form import DealProduceInfoForm
from grid.forms.deal_spatial_form import AddDealSpatialFormSet
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.file_field_with_initial import FileFieldWithInitial, FileInputWithInitial
from grid.forms.investor_formset import InvestorFormSet
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country
from landmatrix.models.investor import InvestorActivityInvolvement, Investor
from landmatrix.models.language import Language
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext

from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.db import transaction
from django.db.models import Model
from django.contrib import messages
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

from wkhtmltopdf import wkhtmltopdf

from datetime import date
import urllib.request
import urllib.error

import os

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class SaveDealView(TemplateView):

    FORMS = [
        ("spatial_data", AddDealSpatialFormSet),            #
        ("general_information", AddDealGeneralForm),        #
        ("employment", AddDealEmploymentForm),              #
        ("investor_info", OperationalStakeholderForm),
        ("data_sources", AddDealDataSourceFormSet),         #
        ("local_communities", DealLocalCommunitiesForm),    #
        ("former_use", DealFormerUseForm),                  #
        ("produce_info", DealProduceInfoForm),              #
        ("water", DealWaterForm),                           #
        ("gender-related_info", DealGenderRelatedInfoForm), #
        ("overall_comment", AddDealOverallCommentForm),     #
        ("action_comment", ChangeDealActionCommentForm),
    ]

    def dispatch(self, request, *args, **kwargs):

        self.request = request
        self.activity = self.get_activity(**kwargs)

        forms = self.get_forms(request.POST)

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # check whether it's valid:
            if all(form.is_valid() for form in forms):
                self.save_form_data(forms, request.FILES)
                # return HttpResponseRedirect('/editor/')
            else:
                print_form_errors(forms)

        context = super().get_context_data(**kwargs)
        context['forms'] = forms
        context['kwargs'] = kwargs
        context['deal_id'] = kwargs.get('deal_id')

        return render_to_response(self.template_name, context, RequestContext(request))

    def save_form_data(self, forms, files):
        groups = []
        for form in forms:
            groups.extend(self.create_attributes_for_form(self.activity, form, files))
        self.save_activity_and_attributes(self.activity, groups)

    @transaction.atomic
    def save_activity_and_attributes(self, activity, groups):
        activity.save()
        ActivityAttributeGroup.objects.filter(fk_activity=activity).delete()
        for group in groups:
            group.fk_activity = activity
            group.save()
        self.create_or_update_operational_stakeholder(activity)

    def create_or_update_operational_stakeholder(self, activity):
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity=activity)
        if len(involvements) > 1:
            raise MultipleObjectsReturned(
                'More than one operational stakeholder for activity {}'.format(str(activity))
            )
        if len(involvements):
            involvement = involvements.last()
            involvement.fk_investor = self.operational_stakeholder
        else:
            involvement = InvestorActivityInvolvement(
                fk_activity=activity, fk_investor=self.operational_stakeholder, fk_status_id=1
            )
        involvement.save()

    def create_attributes_for_form(self,activity, form, files):
        groups = []

        if self.name_of_form(form) == 'investor_info':
            self.operational_stakeholder = form.cleaned_data['operational_stakeholder']

        elif self.name_of_form(form) == 'data_sources':
            self.create_attributes_for_data_sources_formset(activity, form, files, groups)

        elif self.name_of_form(form) == 'spatial_data':
            create_attributes_for_spatial_data_formset(activity, form, groups)

        else:
            if any(form.cleaned_data.values()):
                group = create_attribute_group(activity, form.cleaned_data, self.name_of_form(form))
                groups.append(group)
            else:
                print('no data sent:', self.name_of_form(form))

        return groups

    def name_of_form(self, form):
        return name_of_form(form, self.FORMS)

    def create_attributes_for_data_sources_formset(self, activity, formset, files, groups):
        count = 1
        for sub_form_data in formset.cleaned_data:

            if sub_form_data['type'] and isinstance(sub_form_data['type'], int):
                field = DealDataSourceForm().fields['type']
                choices = dict(field.choices)
                sub_form_data['type'] = str(choices[sub_form_data['type']])

            if sub_form_data['file'] and isinstance(sub_form_data['file'], UploadedFile):
                sub_form_data['file'] = sub_form_data['file'].name

            uploaded = get_file_from_upload(files, count-1)
            if uploaded:
                sub_form_data['file'] = uploaded

            if sub_form_data['url']:
                sub_form_data = handle_url(sub_form_data, self.request)

            group = create_attribute_group(activity, sub_form_data, 'data_source_{}'.format(count))
            count += 1
            groups.append(group)


def get_file_from_upload(files, form_index):
    try:
        key = next(k for k in files.keys() if 'form-{}-file'.format(form_index))
        file = files.getlist(key)[0]
        handle_uploaded_file(file, file.name, FileInputWithInitial.UPLOAD_BASE_DIR)
        return file.name
    except (StopIteration, IndexError, AttributeError):
        return None


def handle_uploaded_file(uploaded_file, file_name, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    with open(base_dir+file_name, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


def handle_url(form_data, request):

    url = form_data['url']

    url_slug = get_url_slug(request, url)

    # if not url_slug or form_data['file'] or url_slug == form_data['file']:
    if not url_slug or url_slug == form_data['file']:
        return

    # Remove file from taggroup
    del form_data['file']

    # Create file for URL
    uploaded_pdf_path = os.path.join(settings.MEDIA_ROOT, "uploads", url_slug)
    if not default_storage.exists(uploaded_pdf_path):
        try:
            # Check if URL changed and no file given
            if url.endswith(".pdf"):
                response = urllib.request.urlopen(url)
                default_storage.save(
                    uploaded_pdf_path, ContentFile(response.read())
                )
            else:
                # Create PDF from URL
                output = wkhtmltopdf(pages=url, output=uploaded_pdf_path)
                print('wkhtmltopdf output:', output)
            form_data['date'] = date.today().strftime("%Y-%m-%d")
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

    return "%s.pdf" % re.sub(r"https|http|ftp|www|", "", slugify(url))


def error_could_not_upload(request, url, message=''):
    messages.error(
        request,
        "<p>Data source <a target='_blank' href='{}'>URL</a> could not be uploaded as a PDF file.</p>"
        "<p>{}</p>"
        "<p>Please upload manually.</p>".format(url, message)
    )


def create_attributes_for_spatial_data_formset(activity, formset, groups):
    count = 1
    for sub_form_data in formset.cleaned_data:
        if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
            sub_form_data['target_country'] = sub_form_data['target_country'].pk
        group = create_attribute_group(activity, sub_form_data, 'spatial_data_{}'.format(count))
        count += 1
        groups.append(group)


def print_form_errors(forms):
    for form in forms:
        if form.is_valid():
            # print(form.__class__.__name__, form.cleaned_data)
            pass
        else:
            print(form.__class__.__name__, 'INVALID! Errors:', form.errors)


def create_attribute_group(activity, form_data, name=None):
    group = ActivityAttributeGroup(
        fk_activity=activity, date=date.today(), name=name,
        attributes = {key: model_to_id(value) for key, value in form_data.items() if value},
        fk_language=Language.objects.get(english_name='English')
    )
    return group


def name_of_form(form, forms):
    for name, Form in forms:
        if Form == form.__class__:
            return name
    raise ValueError('Form %s not in FORMS' % form.__class__.__name__)


def model_to_id(value):
    if isinstance(value, QuerySet):
        return model_to_id(list(value))
    elif isinstance(value, Model):
        return value.pk
    elif isinstance(value, list):
        return [model_to_id(v) for v in value]
    else:
        return value

