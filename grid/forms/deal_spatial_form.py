from pprint import pprint

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.deal import Deal

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import TitleField, LocationWidget, CountryField, CommentInput
from landmatrix.models.region import Region

from django import forms
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _


class DealSpatialForm(BaseForm):

    form_title = _('Location')
    tg_location = TitleField(required=False, label="", initial=_("Location"))
    level_of_accuracy = forms.TypedChoiceField(required=False, label=_("Level of accuracy"), choices=(
        (0, _("---------")),
        (10, _("Country")),
        (20, _("Approximate level")),
        (30, _("Exact location")),
        (40, _("Exact coordinates")),
    ), coerce=int)
    location = forms.CharField(required=False, label=_("Location"), widget=LocationWidget)
    point_lat = forms.CharField(required=False, label=_("Latitude"), widget=forms.TextInput, initial="")
    point_lon = forms.CharField(required=False, label=_("Longitude"), widget=forms.TextInput, initial="")
    target_country = CountryField(required=False, label=_("Target Country"))
    target_region = forms.ModelChoiceField(required=False, label=_("Target Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by("name"))
    tg_location_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)


class DealSpatialBaseFormSet(formset_factory(DealSpatialForm, extra=0)):

    @classmethod
    def get_data(cls, activity):
        if isinstance(activity, Deal):
            activity = activity.activity
        if isinstance(activity, Activity):
            taggroups = ActivityAttributeGroup.objects.\
                filter(fk_activity=activity).filter(attributes__contains=["location"])
        else:
            taggroups = []

        data = {
            'form-TOTAL_FORMS': max(len(taggroups), 1),
            'form-INITIAL_FORMS': max(len(taggroups), 1),
            'form-MAX_NUM_FORMS': 1000
        }
        for i, taggroup in enumerate(taggroups):
            form_data = DealSpatialForm.get_data(activity, taggroup=taggroup)
            # print('DealSpatialBaseFormSet form', i, ':    ', form_data)
            data[i] = form_data
        return data


class AddDealSpatialFormSet(DealSpatialBaseFormSet):

    form_title = _('Location')
    extra = 1

    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
        return ds_taggroups


class ChangeDealSpatialFormSet(AddDealSpatialFormSet):

    form_title = _('Location')
    extra = 0


class PublicViewDealSpatialForm(DealSpatialForm):

    form_title = _('Location')

    class Meta:
        fields = (
            "tg_location", "location", "point_lat", "point_lon", 'tg_location_comment'
        )
        readonly_fields = fields


PublicViewDealSpatialFormSet = formset_factory(PublicViewDealSpatialForm, formset=AddDealSpatialFormSet, extra=0)
