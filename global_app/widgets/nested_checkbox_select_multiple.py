__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from itertools import chain


class NestedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs={}, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label, option_choices) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))
            option = u'<li><label%s>%s %s</label>' % (label_for, rendered_cb, option_label)
            if option_choices:
                option += u'<ul>'
                for j, (option_value, option_label) in enumerate(option_choices):
                    if has_id:
                        final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], "%s-%s"%(i,j)))
                        label_for = u' for="%s"' % final_attrs['id']
                    else:
                        label_for = ''

                    cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                    option_value = force_text(option_value)
                    rendered_cb = cb.render(name, option_value)
                    option_label = conditional_escape(force_text(option_label))
                    option += u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label)

                option += '</ul>'
            option += u'</li>'
            output.append(option)
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))
