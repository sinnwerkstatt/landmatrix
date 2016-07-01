__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import re
from django import forms
from django.utils.safestring import mark_safe

class YearBasedWidget(forms.MultiWidget):
    year_based = True
    widget = forms.TextInput(attrs={"class": "year-based"})

    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedWidget, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            self.widget,
            forms.TextInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        widgets = self.get_widgets()
        multiple = self.get_multiple()
        if value:
            #sorted_values = sorted(values, key=lambda v: v.split(":")[1] if ':' in v else '0')
            values = []
            #for val in value.split("#"):
            #    date_values = []
            for i, val in enumerate(re.split('[#:]', value)):
                if multiple[i % len(widgets)]:
                    values.append(val.split(','))
                else:
                    values.append(val)
            #values.append(date_values)
            #a = len(values) == 1 and values.append(None) or values
            #if 'YearBasedSelectMultipleNumber' in str(self):
            #    raise IOError(values)
            return values
        return [None, None]

    def render_for_template(self):
        raise Exception(self.attrs)

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def get_multiple(self):
        # Check which widgets allow multiple values
        return [hasattr(w, 'allow_multiple_selected') and w.allow_multiple_selected for w in self.get_widgets()]

    def value_from_datadict(self, data, files, name):
        # Find out which widgets allow multiple values
        widgets = self.get_widgets()
        multiple = self.get_multiple()
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = []
        for i, key in enumerate(sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))):
            if multiple[i % len(widgets)]:
                value.append(data.getlist(key))
            else:
                value.append(data.get(key))
        # update widgets
        self.widgets = []
        for i in range(int(len(value)/len(widgets))):
            self.widgets.extend(widgets)
        return value

    def render(self, name, value, attrs={}):
        # update widgets
        if value:
            self.widgets = []
            value = isinstance(value, (list, tuple)) and value or self.decompress(value)
            for i in range(int(len(value)/len(self.get_widgets()))):
                self.widgets.extend(self.get_widgets())
        else:
            self.widgets = self.get_widgets()

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
        widgets_row_count = len(self.get_widgets())
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
            # Append helptext and close reopen div every n element
            if ((i+1) % widgets_row_count) == 0:
                output.append(helptext)
                # Add "Add more" button to first row
                if (i+1) == widgets_row_count:
                    output.append('<a href="javascript:;" class="btn add-ybd add-row"><i class="lm lm-plus"></i> Add more</a>')
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row" style="display:none;"><i class="lm lm-minus"></i> Remove</a>')
                else:
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row"><i class="lm lm-minus"></i> Remove</a>')
                if (i+1) < widgets_count:
                    output.append('</div><div class="input-group">')
        output.append('</div>')
        return mark_safe(self.format_output(output))