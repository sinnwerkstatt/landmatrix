from django.contrib.gis import forms
from django.forms.models import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.country import Country
from landmatrix.models.region import Region
from ol3_widgets.widgets import OSMWidget
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
    AREA_WIDGET_ATTRS = {
        'map_width': 600,
        'map_height': 400,
        'default_zoom': 8,
        'default_lat': 0,
        'default_lon': 0,
        'toggle_map_display': True,
        'geom_type': 'MULTIPOLYGON',
    }

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
    intended_area = forms.MultiPolygonField(
        required=False, label=_("Intended area"),
        widget=OSMWidget(attrs=AREA_WIDGET_ATTRS))
    production_area = forms.MultiPolygonField(
        required=False, label=_("Area in operation"),
        widget=OSMWidget(attrs=AREA_WIDGET_ATTRS))

    tg_location_comment = forms.CharField(
        required=False, label=_("Comment on Location"), widget=CommentInput)

    class Meta:
        name = 'location'

    def __init__(self, *args, **kwargs):
        '''
        If we already have a lat/long, set the default positioning to match.
        '''
        super().__init__(*args, **kwargs)
        initial_lat = self['point_lat'].value()
        initial_lon = self['point_lon'].value()

        # Pass related fields through to the mapwidget
        map_widget_attrs = {}
        if 'location' in self:
            map_widget_attrs['id'] = '{}-map'.format(self['location'].auto_id),

        bound_fields = (
            ('location', 'bound_location_field_id'),
            ('point_lat', 'bound_lat_field_id'),
            ('point_lon', 'bound_lon_field_id'),
            ('target_country', 'bound_target_country_field_id'),
            ('level_of_accuracy', 'bound_level_of_accuracy_field_id'),
        )
        for field, attr in bound_fields:
            if field in self:
                map_widget_attrs[attr] = self[field].auto_id

        if initial_lat or initial_lon:
            area_widget_attrs = self.AREA_WIDGET_ATTRS.copy()

            try:
                lat, lon = float(initial_lat), float(initial_lon)
            except ValueError:
                pass
            else:
                area_widget_attrs['default_lat'] = lat
                area_widget_attrs['default_lon'] = lon
                map_widget_attrs['default_lat'] = lat
                map_widget_attrs['default_lon'] = lon

            self.fields['intended_area'].widget = OSMWidget(
                attrs=area_widget_attrs)
            self.fields['production_area'].widget = OSMWidget(
                attrs=area_widget_attrs)

        self.fields['location'].widget = LocationWidget(
            map_attrs=map_widget_attrs)

    def get_attributes(self, request=None):
        attributes = super().get_attributes()
        # Replace country name with pk
        # FIXME: Why is the coutnry ID getting replaced by the name before
        # Guess that happens by mistake in BaseForm.get_attributes
        if 'target_country' in attributes \
                and not isinstance(attributes['target_country']['value'], int) \
                and not attributes['target_country']['value'].isnumeric():
            target_country = Country.objects.get(
                name=attributes['target_country']['value'])
            attributes['target_country']['value'] = target_country.pk

        # For polygon fields, pass the value directly
        for area_field_name in ('intended_area', 'production_area'):
            if area_field_name in attributes:
                polygon_value = attributes[area_field_name]['value']
                attributes[area_field_name] = {'polygon': polygon_value}

        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group=group, prefix=prefix)

        for area_field_name in ('intended_area', 'production_area'):
            area_attribute = activity.attributes.filter(
                fk_group__name=group, name=area_field_name).first()
            if area_attribute:
                data[area_field_name] = area_attribute.polygon

        return data

    def get_fields_display(self):
        fields = super().get_fields_display()
        # Hide coordinates depending on level of accuracy
        if 'level_of_accuracy' in self:
            accuracy = self['level_of_accuracy']
        else:
            accuracy = ''
        if accuracy in ('Country', 'Administrative region', 'Approximate location'):
            for field in fields:
                if field['name'] in ('point_lat', 'point_lon'):
                    field['hidden'] = True
        return fields


class DealSpatialBaseFormSet(BaseFormSet):

    form_title = _('Location')

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        groups = activity.attributes.filter(fk_group__name__startswith=cls.Meta.name).values_list(
            'fk_group__name', flat=True).order_by('fk_group__name').distinct()

        data = []
        for i, group in enumerate(groups):
            form_data = DealSpatialForm.get_data(activity, group=group)#, prefix='%s-%i' % (cls.Meta.name, i))
            if form_data:
                data.append(form_data)

        return data

    def get_attributes(self, request=None):
        return [form.get_attributes(request) for form in self.forms]

    class Meta:
        name = 'location'


DealSpatialFormSet = formset_factory(
    DealSpatialForm, min_num=1, validate_min=True, extra=0,
    formset=DealSpatialBaseFormSet)
PublicViewDealSpatialFormSet = formset_factory(
    DealSpatialForm, formset=DealSpatialBaseFormSet, extra=0)
