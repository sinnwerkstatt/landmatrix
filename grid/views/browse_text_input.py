__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils.safestring import mark_safe
from django import forms


class BrowseTextInput(forms.TextInput):

    def render(self, name, value, attrs={}):
        output = super(BrowseTextInput, self).render(name, value, attrs)
        output = '<div class="value-wrapper">%s</div>' % output
        output += '<input type="hidden" name="hidden_%s" value="%s"/>' % (name, ",".join(value))
        return mark_safe(output)

    def value_from_datadict(self, data, files, name):

        value = data.getlist(name)
        if not value:
            # could be ybd field, try with suffix _0 and _1 for value|year
            ybd = []
            value = ",".join(data.getlist("%s_0" % name, []))
            if value:
                ybd.append(value)
            year = ",".join(data.getlist("%s_1" % name, []))
            if year:
                if ybd:
                    ybd.append(year)
                else:
                    ybd.append("")
                    ybd.append(year)
            value = ["|".join(ybd)]
        return value or []
