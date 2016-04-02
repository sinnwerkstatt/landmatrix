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
from django.utils.translation import ugettext_lazy as _

from wkhtmltopdf import wkhtmltopdf

from datetime import date
import urllib.request
import urllib.error

import os

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class SaveDealView(TemplateView):
    FORMS = [
        AddDealSpatialFormSet,
        AddDealGeneralForm,
        AddDealEmploymentForm,
        OperationalStakeholderForm,
        AddDealDataSourceFormSet,
        DealLocalCommunitiesForm,
        DealFormerUseForm,
        DealProduceInfoForm,
        DealWaterForm,
        DealGenderRelatedInfoForm,
        AddDealOverallCommentForm,
        ChangeDealActionCommentForm,
    ]
    deal_id = None
    activity = None
    success_message = _('Your changes to the deal have been submitted successfully. The changes will be reviewed and published soon.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        if self.request.method != 'post':
            context['forms'] = self.get_forms()
        context['kwargs'] = self.kwargs
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        forms = self.get_forms(self.request.POST)
        if all(form.is_valid() for form in forms):
            # Delete existing attribute groups
            # FIXME: Why?
            ActivityAttributeGroup.objects.filter(fk_activity=self.activity).delete()
            # Create new attribute groups
            for form in forms:
                attributes = form.get_attributes(request)
                if not attributes:
                    continue
                # Formset?
                if isinstance(attributes, list):
                    for count, form_attributes in enumerate(attributes):
                        ActivityAttributeGroup.objects.create(
                            fk_activity=self.activity,
                            date=date.today(),
                            name='%s_%i' % (form.Meta.name, count),
                            attributes=form_attributes,
                            fk_language=Language.objects.get(english_name='English')
                        )
                # Form
                elif attributes:
                    ActivityAttributeGroup.objects.create(
                        fk_activity=self.activity,
                        date=date.today(),
                        name=form.Meta.name,
                        attributes=attributes,
                        fk_language=Language.objects.get(english_name='English')
                    )
                # Investor form?
                if form.Meta.name == 'investor_info' and form.cleaned_data['operational_stakeholder']:
                    operational_stakeholder = form.cleaned_data['operational_stakeholder']
                    # Update operational stakeholder (involvement)
                    involvements = InvestorActivityInvolvement.objects.filter(fk_activity=self.activity)
                    if len(involvements) > 1:
                        raise MultipleObjectsReturned(
                            'More than one operational stakeholder for activity {}'.format(str(self.activity))
                        )
                    if len(involvements):
                        involvement = involvements.last()
                        involvement.fk_investor = operational_stakeholder
                    else:
                        involvement = InvestorActivityInvolvement(
                            fk_activity=self.activity, fk_investor=operational_stakeholder, fk_status_id=1
                        )
                    involvement.save()
                    messages.success(request, self.success_message.format(self.deal_id))
        else:
            messages.error(request, _('Please correct the error below.'))
        context['forms'] = forms
        return self.render_to_response(context)

    #def create_attributes_for_form(self, activity, form, files):
    #    groups = []
    #
    #    if self.name_of_form(form) == 'investor_info':
    #        self.operational_stakeholder = form.cleaned_data['operational_stakeholder']
    #
    #    elif self.name_of_form(form) == 'data_sources':
    #        self.create_attributes_for_data_sources_formset(activity, form, files, groups)
    #
    #    elif self.name_of_form(form) == 'spatial_data':
    #        create_attributes_for_spatial_data_formset(activity, form, groups)
    #
    #    else:
    #        if any(form.cleaned_data.values()):
    #            group = create_attribute_group(activity, form.cleaned_data, self.name_of_form(form))
    #            groups.append(group)
    #        else:
    #            print('no data sent:', self.name_of_form(form))
    #
    #    return groups

    #def create_attributes_for_data_sources_formset(self, activity, formset, files, groups):
    #    count = 1
    #    for data in formset.cleaned_data:
    #        d = data
    #        if data['type'] and isinstance(data['type'], int):
    #            field = DealDataSourceForm().fields['type']
    #            choices = dict(field.choices)
    #            data['type'] = str(choices[data['type']])
#
    #        if data['file'] and isinstance(data['file'], UploadedFile):
    #            data['file'] = data['file'].name
#
    #        uploaded = get_file_from_upload(files, count-1)
    #        if uploaded:
    #            data['file'] = uploaded
    #        d2 = data
    #        if data['url']:
    #            data = handle_url(data, self.request)
#
    #        if not data:
    #            c = formset.cleaned_data
    #            raise IOError(data)
    #        group = create_attribute_group(activity, data, 'data_source_{}'.format(count))
    #        count += 1
    #        groups.append(group)



#sdef create_attributes_for_spatial_data_formset(activity, formset, groups):
#s    count = 1
#s    for data in formset.cleaned_data:
#s        if data['target_country'] and isinstance(data['target_country'], Country):
#s            data['target_country'] = data['target_country'].pk
#s        group = create_attribute_group(activity, data, 'spatial_data_{}'.format(count))
#s        count += 1
#s        groups.append(group)
#s
#sdef create_attribute_group(activity, form_data, name=None):
#s    group = ActivityAttributeGroup(
#s        fk_activity=activity, date=date.today(), name=name,
#s        attributes = {key: model_to_id(value) for key, value in form_data.items() if value},
#s        fk_language=Language.objects.get(english_name='English')
#s    )
#s    return group


#def name_of_form(form, forms):
#    for name, Form in forms:
#        if Form == form.__class__:
#            return name
#    raise ValueError('Form %s not in FORMS' % form.__class__.__name__)


#def model_to_id(value):
#    if isinstance(value, QuerySet):
#        return model_to_id(list(value))
#    elif isinstance(value, Model):
#        return value.pk
#    elif isinstance(value, list):
#        return [model_to_id(v) for v in value]
#    else:
#        return value