'''
Collected form widgets.

There is a lot of code in here. Most of is just adding attributes and html
though. A lot of this can be moved to templates or made simpler.
Also, I don't think all of these are actually used.
TODO: clean up
'''
import re
from itertools import chain

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, escape

from ol3_widgets.widgets import SerializedMapWidget
from landmatrix.models import Country
from landmatrix.storage import data_source_storage




class TitleWidget(forms.TextInput):
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        return "<h3>%s</h3>" % str(self.initial or "")


class YearBasedWidget(forms.MultiWidget):
    year_based = True
    widget = forms.TextInput(attrs={"class": "year-based"})

    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        if 'attrs' in kwargs:
            self.widget.attrs.update(kwargs.pop('attrs'))
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedWidget, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            self.widget,
            forms.TextInput(attrs={"class": "year-based-year"}),
            forms.CheckboxInput(attrs={"class": "year-based-is-current"})
        ]

    def decompress(self, value):
        widgets = self.get_widgets()
        multiple = self.get_multiple()
        if value:
            values = []
            for i, val in enumerate(re.split('[#:]', value)):
                if multiple[i % len(widgets)]:
                    values.append(val.split(','))
                else:
                    values.append(val)
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
        value = []
        # Grab last item and enumerate, since there can be gaps
        # because of checkboxes not submitting data
        keys = sorted([k for k in data.keys() if re.match(name + '_\d', k)])
        count = len(keys) > 0 and int(keys[-1].replace(name+'_', ''))+1 or 0
        if count % len(widgets) > 0:
            count += 1
        for i in range(count):
            key = name + '_' + str(i)
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
            # Append helptext before last widget (is current)
            if ((i+1) % widgets_row_count) == 0:
                output.append(helptext)
            attrs = dict(final_attrs)
            attrs['class'] = ' '.join([final_attrs.get('class', ''), hasattr(widget, 'attrs') and widget.attrs.get('class', '') or ''])
            output.append(widget.render(name + '_%s' % i, widget_value, attrs))
            # Close reopen div every n element
            if ((i+1) % widgets_row_count) == 0:
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


class YearBasedTextInput(YearBasedWidget):
    widget = None

    def __init__(self, *args, **kwargs):
        self.widget = forms.TextInput(attrs={"class": "year-based"})
        super().__init__(*args, **kwargs)

    def decompress(self, value):
        if value:
            values = value.split("#")

            sorted_values = sorted(values, key=lambda v: v.split(":")[1] if ':' in v else '0')
            splitted = []
            for s in sorted_values:
                splitted.extend(s.split(":"))
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]


class YearBasedSelect(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        self.widget = forms.Select(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedSelect, self).__init__(*args, **kwargs)


class YearBasedSelectMultiple(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        self.widget = forms.SelectMultiple(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedSelectMultiple, self).__init__(*args, **kwargs)


class YearBasedSelectMultipleNumber(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(YearBasedSelectMultipleNumber, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.SelectMultiple(choices=self.choices, attrs={"class": "year-based"}),
            forms.NumberInput(attrs={"class": "year-based", "placeholder": _("Size")}),
            forms.TextInput(attrs={"class": "year-based-year"}),
            forms.CheckboxInput(attrs={"class": "year-based-is-current"})
        ]


class YearBasedMultipleSelect(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        # Remove empty option
        self.choices = filter(lambda c: c[0] != 0, self.choices)
        self.widget = forms.CheckboxSelectMultiple(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedMultipleSelect, self).__init__(*args, **kwargs)


class YearBasedIntegerField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.IntegerField(required=False),
            forms.CharField(required=False),
            forms.BooleanField(required=False)
        ]
        if 'placeholder' in kwargs:
            attrs = {'placeholder': kwargs.pop('placeholder', None)}
        else:
            attrs = {}
        kwargs["widget"] = YearBasedTextInput(help_text=kwargs.pop("help_text", ""), attrs=attrs)
        super(YearBasedIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.IntegerField(required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedIntegerField, self).clean(value)

    def compress(self, data_list):
        """  """
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]


class YearBasedCheckboxInput(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.widget = forms.CheckboxInput(attrs={"class": "year-based"})
        super().__init__(*args, **kwargs)



class TextChoiceInput(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(TextChoiceInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.TextInput(),
            forms.Select(choices=self.choices)
        ]


class MultiTextInput(YearBasedWidget):
    def get_widgets(self):
        return [
            forms.TextInput(),
        ]


class SelectAllCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs={}, choices=()):
        output = u"""
          <label for="select-all-%(id)s">
          <input type="checkbox" name="select-all-%(id)s" class="select" id="select-all-%(id)s">
           Select all
          </label>
          <script type="text/javascript">
            $("#select-all-%(id)s").click(function() {
            $(this).parents(".input-group").find("ul :checkbox").attr("checked", this.checked);
            });
            $(document).ready(function () {
                var checked = $("#select-all-%(id)s").parents(".input-group").find("ul :checked").length;
                var all = $("#select-all-%(id)s").parents(".input-group").find("ul :checkbox").length
                if (checked == all) {
                    $("#select-all-%(id)s").attr("checked", "checked");
                }
            });

          </script>
        """ % {
            "id": attrs.get("id"),
        }
        output += super(SelectAllCheckboxSelectMultiple, self).render(name, value, attrs)
        return mark_safe(output)


class PrimaryInvestorSelect(forms.Select):

    def render(self, name, value, attrs={}, choices=()):
        output = super(PrimaryInvestorSelect, self).render(name, value, attrs, choices)
        output += """
            <a class="btn change-investor" id="change_id_primary_investor" target="_blank" href='/browse/primary-investor/%(value)s/'><i class="icon-pencil"></i> Edit Primary-Investor</a>
            <a class="btn add-investor" id="add_id_primary_investor" target="_blank" href='/add/primary-investor/'><i class="icon-plus"></i> Add Primary-Investor</a>
            <script type="text/javascript">
            // Update change link href
            $(".%(name)s select").change(function () {
                var l = $(this).parent().find("a.change-investor");
                var v = $(this).find("option:selected").val();
                if (v != "") {
                  l.attr("href", l.attr("href").replace(/\d+/, v));
                }
            });
            // Handler for change link
            $("a.change-investor").click(function (e) {
              e.preventDefault();
              showChangeInvestorPopup(this);
              return false;
            });
            // Handler for add link
            $("a.add-investor").click(function (e) {
              e.preventDefault();
              showAddInvestorPopup(this);
              return false;
            });
            </script>
        """ % {
            "value": value and value or "0",
            "name": name
        }
        return output


class NumberInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({
            'type': 'number',
            'class': 'form-control'
        })
        return super(NumberInput, self).render(name, value, attrs)


class FileInputWithInitial(forms.ClearableFileInput):
    displayed_chars = 40
    existing_file_template = '<a class="input-group-addon" href="{url}" target="_blank" title="' + str(_('Current file')) \
        + ' class="toggle-tooltip"><i class="fa fa-file-pdf-o"></i></a>'
    new_upload_template = "{}-new"

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        output = ""

        if value:
            if self.is_initial(value):
                # previously uploaded file
                value_name = str(value.name)
                value_url = value.url
            else:
                value_name = str(value)
                value_url = data_source_storage.url(value)

            if len(value_name) > self.displayed_chars:
                display_name = value_name[:self.displayed_chars] + '...'
            else:
                display_name = value_name

            output += self.existing_file_template.format(label=_("Saved file"),
                                                         url=value_url,
                                                         name=display_name)

        file_input = super().render(self.new_upload_template.format(name),
                                    None, attrs)
        output += file_input

        return output

    def value_from_datadict(self, data, files, name):
        new_file_name = self.new_upload_template.format(name)

        try:
            value = files[new_file_name]
        except KeyError:
            value = None

        return value


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


class DecimalInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({
            'type': 'number',
            'step': 'any',
            'class': 'form-control'
        })
        return super(DecimalInput, self).render(name, value, attrs)


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
            code = Country.objects.defer('geom').get(pk=option_value).code_alpha2
        else:
            code = ""
        return u'<option value="%s" title="%s" %s>%s</option>' % (
            escape(option_value), code, selected_html,
            conditional_escape(force_text(option_label)))


class CommentInput(forms.Textarea):
    def render(self, name, value, attrs={}):
        attrs.update({'rows': '3', 'class': 'form-control'})
        return super(CommentInput, self).render(name, value, attrs)


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


class AreaWidget(forms.MultiWidget):
    '''
    Area widget includes a map, and a shapefile upload field.
    '''

    MAP_WIDGET_ATTRS = {
        'map_width': 600,
        'map_height': 400,
        'initial_zoom': 8,
        'initial_center_lat': 0,
        'initial_center_lon': 0,
        'show_layer_switcher': True,
        'geom_type': 'MULTIPOLYGON',
    }
    FILE_WIDGET_ATTRS = {
        'multiple': True,
    }

    def __init__(self, *args, **kwargs):
        self.initially_hidden = kwargs.pop('initially_hidden', True)
        map_attrs = self.MAP_WIDGET_ATTRS.copy()
        map_attrs.update(kwargs.pop('map_attrs', {}))
        file_attrs = self.FILE_WIDGET_ATTRS.copy()
        file_attrs.update(kwargs.pop('file_attrs', {}))

        widgets = [
            SerializedMapWidget(attrs=map_attrs),
            forms.ClearableFileInput(attrs=file_attrs),
        ]
        super().__init__(widgets, *args, **kwargs)

    def render(self, name, value, attrs=None):
        '''
        Overridden to pass name to format_output, so we can do js things
        with the map.
        '''
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
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(
                widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(name, output))

    def decompress(self, value):
        return [value, False]

    def format_output(self, name, rendered_widgets):
        if self.initially_hidden:
            container_style = 'display: none;'
            show_hide_link_text = _('Show area')
            show_hide_link_alt_text = _('Hide area')
        else:
            container_style = ''
            show_hide_link_text = _('Hide area')
            show_hide_link_alt_text = _('Show area')

        # TODO: move the JS into a static file
        js = '''
            var container = jQuery('#{name}-container');
            var showLink = container.next('a.show-hide-area');

            showLink.on('click', function (event) {{
                event.preventDefault();
                $this = jQuery(this);
                var target = jQuery('#' + $this.data('divId'));
                var oldText = $this.text();
                var newText = $this.data('alternate');

                target.toggle();
                $this.text(newText);
                $this.data('alternate', oldText);

                if (target.is(':visible')) {{
                    var mapWidget = jQuery('#id_{name}_0').data('mapWidget');
                    mapWidget.map.updateSize();
                    mapWidget.positionMap();
                }}

            }});
        '''.format(name=name)
        output = '''
        <div id="{name}-container" style="{style}">
            {map_widget}
            <br>
            {file_widget}
        </div>
        <a href="#" class="show-hide-area pull-right"
            data-alternate="{link_alt_text}"
            data-div-id="{name}-container">{link_text}</a>
        <script>
            {js}
        </script>
        '''.format(
            name=name, style=container_style, map_widget=rendered_widgets[0],
            file_widget=rendered_widgets[1], link_text=show_hide_link_text,
            link_alt_text=show_hide_link_alt_text, js=js)

        return output
