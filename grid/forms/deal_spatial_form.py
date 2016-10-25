from django.contrib.gis import forms
from django.forms.models import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.country import Country
from landmatrix.models.region import Region
from ol3_widgets.widgets import LocationWidget, MapWidget, SerializedMapWidget
from grid.fields import TitleField, CountryField
from grid.widgets import CommentInput
from grid.gis import parse_shapefile
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
        'initial_zoom': 8,
        'initial_center_lat': 0,
        'initial_center_lon': 0,
        'toggle_map_display': True,
        'show_layer_switcher': True,
        'geom_type': 'MULTIPOLYGON',
    }
    POLYGON_FIELDS = (
        'contract_area',
        'intended_area',
        'production_area',
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
    contract_area = forms.MultiPolygonField(
        required=False, label=_("Contract area"),
        widget=SerializedMapWidget(attrs=AREA_WIDGET_ATTRS))
    contract_area_shapefile = forms.FileField(
        required=False, label=_("Contract area shapefile"),
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    intended_area = forms.MultiPolygonField(
        required=False, label=_("Intended area"),
        widget=SerializedMapWidget(attrs=AREA_WIDGET_ATTRS))
    intended_area_shapefile = forms.FileField(
        required=False, label=_("Intended area shapefile"),
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    production_area = forms.MultiPolygonField(
        required=False, label=_("Area in operation"),
        widget=SerializedMapWidget(attrs=AREA_WIDGET_ATTRS))
    production_area_shapefile = forms.FileField(
        required=False, label=_("Area in operation shapefile"),
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    tg_location_comment = forms.CharField(
        required=False, label=_("Comment on Location"), widget=CommentInput)

    class Meta:
        name = 'location'

    def __init__(self, *args, **kwargs):
        '''
        Pass the values we need through to map widgets
        '''
        super().__init__(*args, **kwargs)

        lat_lon_attrs = self.get_default_lat_lon_attrs()
        if lat_lon_attrs:
            area_widget_attrs = self.AREA_WIDGET_ATTRS.copy()
            area_widget_attrs.update(lat_lon_attrs)
            for polygon_field in self.POLYGON_FIELDS:
                widget = SerializedMapWidget(attrs=area_widget_attrs)
                self.fields[polygon_field].widget = widget

        location_attrs = self.get_location_map_widget_attrs(
            attrs=lat_lon_attrs)
        # Public field gets a mapwidget, so check for that
        if isinstance(self.fields['location'].widget, MapWidget):
            self.fields['location'].widget = MapWidget(attrs=location_attrs)
        else:
            self.fields['location'].widget = LocationWidget(
                map_attrs=location_attrs)

    def get_location_map_widget_attrs(self, attrs=None):
        map_widget_attrs = {
            'show_layer_switcher': True,
        }

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

        if attrs:
            map_widget_attrs.update(attrs)

        return map_widget_attrs

    def get_default_lat_lon_attrs(self):
        attrs = {}
        try:
            lat = float(self['point_lat'].value())
        except ValueError:
            lat = None

        try:
            lon = float(self['point_lon'].value())
        except ValueError:
            lon = None

        if lat and lon:
            attrs.update({
                'initial_center_lon': lon,
                'initial_center_lat': lat,
                'initial_point': [lon, lat],
            })

        return attrs

    def clean_area_shapefile(self, attr_name):
        value = self.cleaned_data[attr_name]

        field = self[attr_name]
        if field.html_name in self.files:
            shapefile_data = self.files.getlist(field.html_name)
            try:
                value = parse_shapefile(shapefile_data)
            except ValueError as err:
                raise forms.ValidationError(
                    _('Error parsing shapefile: %s') % err)

        return value

    def clean_contract_area_shapefile(self):
        return self.clean_area_shapefile('contract_area_shapefile')

    def clean_intended_area_shapefile(self):
        return self.clean_area_shapefile('intended_area_shapefile')

    def clean_production_area_shapefile(self):
        return self.clean_area_shapefile('production_area_shapefile')

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
        for field_name in self.POLYGON_FIELDS:
            shapefile_field_name = '{}_shapefile'.format(field_name)
            polygon_value = self.cleaned_data.get(shapefile_field_name)
            if polygon_value is None:
                polygon_value = attributes.get(field_name, {}).get('value')

            if polygon_value is not None:
                attributes[field_name] = {'polygon': polygon_value}

        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group=group, prefix=prefix)

        for area_field_name in cls.POLYGON_FIELDS:
            area_attribute = activity.attributes.filter(
                fk_group__name=group, name=area_field_name).first()
            if area_attribute:
                data[area_field_name] = area_attribute.polygon

        return data

    def get_fields_display(self):
        fields = super().get_fields_display()
        # Hide coordinates depending on level of accuracy
        accuracy = self.initial.get('level_of_accuracy', '')
        if accuracy in ('Country', 'Administrative region', 'Approximate location'):
            for field in fields:
                if field['name'] in ('point_lat', 'point_lon'):
                    field['hidden'] = True
        return fields


class PublicDealSpatialForm(DealSpatialForm):
    AREA_WIDGET_ATTRS = {
        'map_width': 600,
        'map_height': 400,
        'default_zoom': 8,
        'default_lat': 0,
        'default_lon': 0,
        'toggle_map_display': True,
        'geom_type': 'MULTIPOLYGON',
        'disable_drawing': True,
    }

    location = forms.CharField(
        required=True, label=_("Location"), widget=MapWidget)

    def get_location_map_widget_attrs(self, attrs=None):
        location_attrs = super().get_location_map_widget_attrs(attrs=attrs)
        location_attrs['disable_drawing'] = True

        return location_attrs


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
        return [form.get_attributes(request=request) for form in self.forms]

    class Meta:
        name = 'location'


DealSpatialFormSet = formset_factory(
    DealSpatialForm, min_num=1, validate_min=True, extra=0,
    formset=DealSpatialBaseFormSet)
PublicViewDealSpatialFormSet = formset_factory(
    PublicDealSpatialForm, formset=DealSpatialBaseFormSet, extra=0)
