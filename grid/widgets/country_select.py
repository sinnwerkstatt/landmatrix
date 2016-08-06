__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.country import Country

from django import forms
from django.utils.encoding import force_text
from django.utils.html import escape, conditional_escape


class CountrySelect(forms.Select):

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        if option_value:
            code = Country.objects.get(pk=option_value).code_alpha2
        else:
            code = ""
        return u'<option value="%s" title="%s" %s>%s</option>' % (
            escape(option_value), code, selected_html,
            conditional_escape(force_text(option_label)))
