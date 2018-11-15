from django.contrib.gis import forms
from django.forms.models import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _

from ol3_widgets.widgets import LocationWidget, MapWidget
from grid.fields import TitleField, CountryField, AreaField
from grid.widgets import CommentInput, AreaWidget
from grid.gis import parse_shapefile
from .base_form import BaseForm


class DealSpatialForm(BaseForm):
    exclude_in_export = ['contract_area', 'intended_area', 'production_area']
    ACCURACY_CHOICES = (
        ("", _("---------")),
        ("Country", _("Country")),
        ("Administrative region", _("Administrative region")),
        ("Approximate location", _("Approximate location")),
        ("Exact location", _("Exact location")),
        ("Coordinates", _("Coordinates")),
    )
    AREA_FIELDS = (
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
        required=False, label=_("Location"), widget=LocationWidget)
    point_lat = forms.CharField(
        required=False, label=_("Latitude"), widget=forms.TextInput,
        initial="")
    point_lon = forms.CharField(
        required=False, label=_("Longitude"), widget=forms.TextInput,
        initial="")
    facility_name = forms.CharField(
        required=False, label=_("Facility name"), widget=forms.TextInput,
        initial="")
    target_country = CountryField(required=False, label=_("Target country"))
    #target_region = forms.ModelChoiceField(
    #    required=False, label=_("Target Region"), widget=forms.HiddenInput,
    #    queryset=Region.objects.all().order_by("name"))
    location_description = forms.CharField(
        required=False, label=_("Location description"),
        widget=forms.TextInput, initial="")
    contract_area = AreaField(required=False, label=_("Contract area"))
    intended_area = AreaField(required=False, label=_("Intended area"))
    production_area = AreaField(required=False, label=_("Area in operation"))

    tg_location_comment = forms.CharField(
        required=False, label=_("Comment on location"), widget=CommentInput)

    class Meta:
        name = 'location'

    def __init__(self, *args, **kwargs):
        '''
        Pass the values we need through to map widgets
        '''
        super().__init__(*args, **kwargs)

        lat_lon_attrs = self.get_default_lat_lon_attrs()

        # Bind area maps to the main location map
        area_attrs = {
            'bound_map_field_id': '{}-map'.format(self['location'].html_name)
        }
        area_attrs.update(lat_lon_attrs)

        location_attrs = self.get_location_map_widget_attrs()
        location_attrs.update(lat_lon_attrs)

        if area_attrs:
            for polygon_field in self.AREA_FIELDS:
                widget = AreaWidget(map_attrs=area_attrs)
                self.fields[polygon_field].widget = widget

        # Public field gets a mapwidget, so check for that
        if isinstance(self.fields['location'].widget, MapWidget):
            self.fields['location'].widget = MapWidget(attrs=location_attrs)
        else:
            self.fields['location'].widget = LocationWidget(
                map_attrs=location_attrs)

    def get_location_map_widget_attrs(self):
        attrs = {
            'show_layer_switcher': True,
        }

        bound_fields = (
            ('location', 'bound_location_field_id'),
            ('target_country', 'bound_target_country_field_id'),
            ('level_of_accuracy', 'bound_level_of_accuracy_field_id'),
            ('point_lat', 'bound_lat_field_id'),
            ('point_lon', 'bound_lon_field_id'),
        )
        for field, attr in bound_fields:
            try:
                attrs[attr] = self[field].auto_id
            except KeyError:
                pass

        return attrs

    def get_default_lat_lon_attrs(self):
        attrs = {}
        try:
            lat = float(self['point_lat'].value() or 0)
        except ValueError:
            lat = None

        try:
            lon = float(self['point_lon'].value() or 0)
        except ValueError:
            lon = None

        if lat and lon:
            attrs.update({
                'initial_center_lon': lon,
                'initial_center_lat': lat,
                'initial_point': [lon, lat],
            })

        return attrs

    def clean_area_field(self, field_name):
        value = self.cleaned_data[field_name]

        try:
            # Check if we got a file here, as
            value.name
            value.size
        except AttributeError:
            value_is_file = False
        else:
            value_is_file = True

        if value_is_file:
            # Files are the second widget, so append _1
            field_name = '{}_1'.format(self[field_name].html_name)
            shapefile_data = hasattr(self.files, 'getlist') and self.files.getlist(field_name) or self.files[field_name]
            try:
                value = parse_shapefile(shapefile_data)
            except ValueError as err:
                error_msg = _('Error parsing shapefile: %s') % err
                raise forms.ValidationError(error_msg)

        return value

    def clean_contract_area(self):
        return self.clean_area_field('contract_area')

    def clean_intended_area(self):
        return self.clean_area_field('intended_area')

    def clean_production_area(self):
        return self.clean_area_field('production_area')

    def get_attributes(self, request=None):
        attributes = super().get_attributes()

        # For polygon fields, pass the value directly
        for field_name in self.AREA_FIELDS:
            polygon_value = self.cleaned_data.get(field_name)
            attributes[field_name] = {'polygon': polygon_value}

        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group=group, prefix=prefix)

        for area_field_name in cls.AREA_FIELDS:
            area_attribute = activity.attributes.filter(
                fk_group__name=group, name=area_field_name).first()
            if area_attribute:
                data[area_field_name] = area_attribute.polygon

        return data

    def get_fields_display(self, user=None):
        fields = super().get_fields_display(user=user)
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
        'geom_type': 'MULTIPOLYGON',
        'disable_drawing': True,
    }

    location = forms.CharField(
        required=True, label=_("Location"), widget=MapWidget)

    def get_location_map_widget_attrs(self):
        location_attrs = super().get_location_map_widget_attrs()
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

    @property
    def meta(self):
        # Required for template access to Meta class
        return hasattr(self, 'Meta') and self.Meta or None

    class Meta:
        name = 'location'


DealSpatialFormSet = formset_factory(
    DealSpatialForm, min_num=1, validate_min=True, extra=0,
    formset=DealSpatialBaseFormSet)
PublicViewDealSpatialFormSet = formset_factory(
    PublicDealSpatialForm, formset=DealSpatialBaseFormSet, extra=0)
