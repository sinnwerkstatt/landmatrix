__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.forms.util import flatatt


class LocationWidget(forms.TextInput):

    def render(self, name, value, attrs={}):
        final_attrs = self.build_attrs(attrs, name=name)
        return """
        <input id="id_%(name)s" name="%(name)s" type="text" value="%(value)s" %(attrs)s/>
        <div class="map" style="width:470px; height:400px; margin-bottom: 30px;"></div>
        """ % {
            "name": str(name or ""),
            "value": str(value or ""),
            "attrs": flatatt(final_attrs)
        }
