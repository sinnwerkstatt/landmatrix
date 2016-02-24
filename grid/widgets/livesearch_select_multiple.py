__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from itertools import chain


class LivesearchSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs={}, choices=()):
        output = ['<input type="text" class="livesearch multiple"></input>']
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output.append(u'<ul>')
        # Normalize to strings
        str_values = set([force_text(v.id) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            option_value = force_text(option_value)
            option_label = conditional_escape(force_text(option_label))
            output.append(u'<li><a href="#%s" %s>%s</a>%s</li>' % (
                option_value,
                option_value in str_values and "class=\"selected-subsidiary\"" or "",
                option_label,
                option_value in str_values and "<input type=\"hidden\" name=\"%s\" value=\"%s\">" % (name, option_value) or ""
            ))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))
