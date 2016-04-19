from django import forms
from django.forms.utils import flatatt


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class LocationWidget(forms.TextInput):

    def render(self, name, value, attrs={}):
        final_attrs = self.build_attrs(attrs, name=name)
        return """
        <input id="id_%(name)s" name="%(name)s" type="text" value="%(value)s" %(attrs)s/>
        <div class="maptemplate"></div>
        """ % {
            "name": str(name or ""),
            "value": str(value or ""),
            "attrs": flatatt(final_attrs)
        }
