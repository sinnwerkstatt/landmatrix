from django import forms

from ol3_widgets.widgets import MapWidget


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class LocationWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        map_attrs = {}
        if 'map_attrs' in kwargs:
            map_attrs = kwargs.pop('map_attrs')

        super().__init__(*args, **kwargs)
        self.map_attrs = map_attrs

    def render(self, name, value, attrs=None):
        map_widget = MapWidget(attrs=self.map_attrs)
        map_name = '{}-map'.format(name)

        rendered_location = super().render(name, value, attrs=attrs)
        rendered_map = map_widget.render(map_name, None)
        output = '<div>{}</div><div>{}</div>'.format(
            rendered_location, rendered_map)

        return output
