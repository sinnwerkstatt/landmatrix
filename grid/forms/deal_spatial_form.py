from django import forms
from django.forms.models import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country, Region
from grid.widgets import TitleField, LocationWidget, CountryField, CommentInput
from .base_form import BaseForm


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealSpatialForm(BaseForm):
    ACCURACY_CHOICES = (
        ("", _("---------")),
        ("Country", _("Country")),
        ("Administrative region", _("Administrative region")),
        ("Approximate location", _("Approximate location")),
        ("Exact location", _("Exact location")),
        ("Coordinates", _("Coordinates")),
    )
    form_title = _('Location')
    tg_location = TitleField(
        required=False, label="", initial=_("Location"))
    level_of_accuracy = forms.ChoiceField(
        required=False, label=_("Spatial accuracy level"),
        choices=ACCURACY_CHOICES)
    location = forms.CharField(
        required=True, label=_("Location"), widget=LocationWidget)
    point_lat = forms.CharField(
        required=False, label=_("Latitude"), widget=forms.TextInput,
        initial="")
    point_lon = forms.CharField(
        required=False, label=_("Longitude"), widget=forms.TextInput,
        initial="")
    facility_name = forms.CharField(
        required=False, label=_("Facility name"), widget=forms.TextInput,
        initial="")
    target_country = CountryField(required=False, label=_("Target Country"))
    target_region = forms.ModelChoiceField(
        required=False, label=_("Target Region"), widget=forms.HiddenInput,
        queryset=Region.objects.all().order_by("name"))
    location_description = forms.CharField(
        required=False, label=_("Location description"),
        widget=forms.TextInput, initial="")
    tg_location_comment = forms.CharField(
        required=False, label=_("Location comments"), widget=CommentInput)

    class Meta:
        name = 'spatial_data'

    def get_attributes(self, request=None):
        attributes = super().get_attributes()
        # Validate target country
        #if 'target_country' in attributes \
        #        and not isinstance(attributes['target_country'], int) \
        #        and not attributes['target_country'].isnumeric():
        #    target_country = Country.objects.get(
        #        name=attributes['target_country'])
        #    attributes['target_country'] = target_country.pk
        return attributes


class DealSpatialBaseFormSet(BaseFormSet):

    form_title = _('Location')
    prefix = 'location'

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        groups = activity.attributes.filter(
            fk_group__name__startswith=cls.prefix).values_list(
            'fk_group__name').distinct()
        data = []
        for i, group in enumerate(groups):
            form_data = DealSpatialForm.get_data(activity, group=group[0])
            if form_data:
                data.append(form_data)
        return data

    def get_attributes(self, request=None):
        return [form.get_attributes(request) for form in self.forms]

    class Meta:
        name = 'spatial_data'


DealSpatialFormSet = formset_factory(DealSpatialForm, min_num=1,
                                     validate_min=True, extra=0,
                                     formset=DealSpatialBaseFormSet)
PublicViewDealSpatialFormSet = formset_factory(DealSpatialForm,
                                               formset=DealSpatialBaseFormSet,
                                               extra=0)
