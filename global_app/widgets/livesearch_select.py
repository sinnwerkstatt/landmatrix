__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from itertools import chain


class LivesearchSelect(forms.RadioSelect):

    def render(self, name, value, attrs={}, choices=()):
        output = [
            '<a href="#" class="livesearch"><i class="lm lm-search"></i></a>',
            '<p class="livesearch-active"></p>',
            '<input type="hidden" name="%s" value="%s">' % (name, value)]
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output.append(u'<ul style="display:none">')
        value = force_text(value)
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            option_value = force_text(option_value)
            option_label = conditional_escape(force_text(option_label))
            output.append(u'<li><a href="#%s" %s>%s</a></li>' % (
                option_value,
                option_value == value and "class=\"active\"" or "",
                option_label
            ))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))
