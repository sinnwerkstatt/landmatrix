__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from global_app.widgets import TitleField, LocationWidget, CountryField, CommentInput
from landmatrix.models.region import Region

from django import forms
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _


class DealSpatialForm(BaseForm):

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

DealSpatialBaseFormSet = formset_factory(DealSpatialForm, extra=1)


class AddDealSpatialFormSet(DealSpatialBaseFormSet):

    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
        return ds_taggroups

    @classmethod
    def get_data(cls, activity):
        taggroups = activity.a_tag_group_set.filter(fk_a_tag__fk_a_value__value__contains="location").order_by("fk_a_tag__fk_a_value__value")
        data = []
        for i, taggroup in enumerate(taggroups):
            data.append(DealSpatialForm.get_data(activity, tg=taggroup))
        return data


class ChangeDealSpatialFormSet(AddDealSpatialFormSet):

    extra = 0
