__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.safestring import mark_safe


class YearBasedWidget(forms.MultiWidget):

    year_based = True

    def render_for_template(self):
        raise Exception(self.attrs)

    def get_widgets(self):
        return []

    def render(self, name, value, attrs={}):
        # update widgets
        if value:
            self.widgets = []
            value = isinstance(value, (list, tuple)) and value or self.decompress(value)
            for i in range(int(len(value)/2)):
                self.widgets.extend(self.get_widgets())

        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        helptext = self.help_text and "<span class=\"helptext input-group-addon\">%s</span>" % str(self.help_text) or ""
        widgets_count = len(self.widgets)
        output.append('<div class="input-group">')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            attrs = dict(final_attrs)
            attrs['class'] = ' '.join([final_attrs.get('class', ''), widget.attrs.get('class', '')])
            output.append(widget.render(name + '_%s' % i, widget_value, attrs))
            # Append helptext and close reopen div every second element
            if ((i+1) % 2 == 0):
                output.append(helptext)
                # Add "Add more" button to first row
                if i == 1:
                    output.append('<a href="javascript:;" class="btn add-ybd add-row"><i class="lm lm-plus"></i> Add more</a>')
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row" style="display:none;"><i class="lm lm-minus"></i> Remove</a>')
                else:
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row"><i class="lm lm-minus"></i> Remove</a>')
                if (i+1) < widgets_count:
                    output.append('</div><div class="input-group">')
        output.append('</div>')
        return mark_safe(self.format_output(output))
