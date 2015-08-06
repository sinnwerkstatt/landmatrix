
from itertools import chain
import re

from django.utils.html import escape, conditional_escape
from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from landmatrix.models import Country, PrimaryInvestor

def force_unicode(string): return force_text(string)

class NumberInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({'type': 'number'})
        return super(NumberInput, self).render(name, value, attrs)

class DecimalInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({'type': 'number', 'step': 'any'})
        return super(DecimalInput, self).render(name, value, attrs)

class CommentInput(forms.Textarea):
    def render(self, name, value, attrs={}):
        attrs.update({'rows': '3'})
        return super(CommentInput, self).render(name, value, attrs)

class TitleWidget(forms.TextInput):
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super(TitleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        return "<h3>%s</h3>" % unicode(self.initial or "")

class TitleField(forms.CharField):
    widget = forms.HiddenInput

    def __init__(self, *args, **kwargs):
        self.widget = TitleWidget(initial=kwargs.get("initial"))
        super(TitleField, self).__init__(*args, **kwargs)

class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % obj.get_full_name() or obj.username

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

class NestedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs={}, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label, option_choices) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
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
                    option_value = force_unicode(option_value)
                    rendered_cb = cb.render(name, option_value)
                    option_label = conditional_escape(force_unicode(option_label))
                    option += u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label)

                option += '</ul>'
            option += u'</li>'
            output.append(option)
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

class SelectAllCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs={}, choices=()):
        output = u"""
          <label for="select-all-%(id)s">
          <input type="checkbox" name="select-all-%(id)s" class="select" id="select-all-%(id)s">
           Select all
          </label>
          <script type="text/javascript">
            $("#select-all-%(id)s").click(function() {
            $(this).parents(".input-append").find("ul :checkbox").attr("checked", this.checked);
            });
            $(document).ready(function () {
                var checked = $("#select-all-%(id)s").parents(".input-append").find("ul :checked").length;
                var all = $("#select-all-%(id)s").parents(".input-append").find("ul :checkbox").length
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

class NestedMultipleChoiceField(forms.MultipleChoiceField):
    widget = NestedCheckboxSelectMultiple
    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        for k, v, c in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == smart_unicode(k2):
                        return True
            else:
                if value == smart_unicode(k):
                    return True
                elif c:
                    for k2, v2 in c:
                        if value == smart_unicode(k2):
                            return True
        return False

    def get_value(self, key):
        for k, v, c in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if key == smart_unicode(k2):
                        return v2
            else:
                if key == smart_unicode(k):
                    return v
                elif c:
                    for k2, v2 in c:
                        if k == smart_unicode(k2):
                            return v2

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
        helptext = self.help_text and "<span class=\"helptext add-on last\">%s</span>"%unicode(self.help_text) or ""
        widgets_count = len(self.widgets)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            # Append helptext and close reopen div every second element
            if ((i+1) % 2 == 0):
                output.append(helptext)
                # Add "Add more" button to first row
                if i == 1:
                    output.append('<a href="javascript:;" class="btn add-ybd add-row"><i class="icon-plus"></i> Add more</a>')
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row" style="display:none;"><i class="icon-remove"></i> Remove</a>')
                else:
                    output.append('<a href="javascript:;" class="btn remove-ybd delete-row"><i class="icon-remove"></i> Remove</a>')
                if (i+1) < widgets_count:
                    output.append('</div><div class="input-append">')
        return mark_safe(self.format_output(output))

class YearBasedSelect(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        return super(YearBasedSelect, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.Select(choices=self.choices, attrs={"class": "year-based"}),
            forms.TextInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            splitted = re.split("[:\|]", value)
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]
        return value


class YearBasedMultipleSelect(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        # Remove empty option
        self.choices = filter(lambda c: c[0] != 0, self.choices)
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        return super(YearBasedMultipleSelect, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.CheckboxSelectMultiple(choices=self.choices, attrs={"class": "year-based"}),
            forms.TextInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            splitted = re.split("[:\|]", value)
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]
        return value


class YearBasedChoiceField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.ChoiceField(choices=kwargs["choices"], required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedSelect(choices=kwargs.pop("choices"),help_text=kwargs.pop("help_text", ""))
        return super(YearBasedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/2):
                self.fields.extend([forms.ChoiceField(choices=self.choices, required=False), forms.CharField(required=False)])
        return super(YearBasedChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)/2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (unicode(data_list[i]), unicode(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.ChoiceField(choices=self.choices, required=False), forms.CharField(required=False)]

    # def prepare_value(self, value):
    #     raise IOError, "ok"

class YearBasedTextInput(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        return super(YearBasedTextInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            NumberInput(attrs={"class": "year-based"}),
            NumberInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            sorted_values = sorted(value.split("|"), key=lambda v: v.split(":")[1] and int(v.split(":")[1]) or 0)
            splitted = []
            for s in sorted_values:
                splitted.extend(s.split(":"))
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]

        # update widgets
        self.widgets = []
        for i in range(len(value)/2):
            self.widgets.extend([NumberInput(attrs={"class": "year-based"}), NumberInput(attrs={"class": "year-based-year"})])
        return value

class YearBasedIntegerField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.IntegerField(required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedTextInput(help_text=kwargs.pop("help_text", ""))
        return super(YearBasedIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/2):
                self.fields.extend([forms.IntegerField(required=False), forms.CharField(required=False)])
        return super(YearBasedIntegerField, self).clean(value)

    def compress(self, data_list):
        """  """
        if data_list:
            yb_data = []
            for i in range(len(data_list)/2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (unicode(data_list[i]), unicode(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]

class YearBasedCheckboxInput(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        return super(YearBasedCheckboxInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.CheckboxInput(attrs={"class": "year-based"}),
            NumberInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            splitted = re.split("[:\|]", value)
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]
        # update widgets
        self.widgets = []
        for i in range(len(value)/2):
            self.widgets.extend([forms.CheckboxInput(attrs={"class": "year-based"}), NumberInput(attrs={"class": "year-based-year"})])
        return value


class YearBasedBooleanField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.BooleanField(required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedCheckboxInput(help_text=kwargs.pop("help_text", ""))
        return super(YearBasedBooleanField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/2):
                self.fields.extend([forms.BooleanField(required=False), forms.CharField(required=False)])
        return super(YearBasedBooleanField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)/2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (unicode(data_list[i]), unicode(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]

class CountrySelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
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
            conditional_escape(force_unicode(option_label)))

class CountryField(forms.ModelChoiceField):
    widget = CountrySelect(attrs={"readonly":"readonly"})

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Country.objects.all().order_by("name")
        return super(CountryField, self).__init__(*args, **kwargs)

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

class LivesearchSelect(forms.RadioSelect):
    def render(self, name, value, attrs={}, choices=()):
        output = [
            '<a href="#" class="livesearch"><i class="icon-search"></i></a>',
            '<p class="livesearch-active"></p>',
            '<input type="hidden" name="%s" value="%s">' % (name, value)]
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output.append(u'<ul style="display:none">')
        value = force_unicode(value)
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            option_value = force_unicode(option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><a href="#%s" %s>%s</a></li>' % (
                option_value,
                option_value == value and "class=\"active\"" or "",
                option_label
            ))
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
        str_values = set([force_unicode(v.id) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            option_value = force_unicode(option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><a href="#%s" %s>%s</a>%s</li>' % (
                option_value,
                option_value in str_values and "class=\"selected-subsidiary\"" or "",
                option_label,
                option_value in str_values and "<input type=\"hidden\" name=\"%s\" value=\"%s\">" % (name, option_value) or ""
            ))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

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
              showChangePopup(this);
              return false;
            });
            // Handler for add link
            $("a.add-investor").click(function (e) {
              e.preventDefault();
              showAddAnotherPopup(this);
              return false;
            });
            </script>
        """ % {
            "value": value and value or "0",
            "name": name
        }
        return output

class PrimaryInvestorField(forms.ChoiceField):
    widget = PrimaryInvestorSelect
    # TODO: fix
    #queryset = PrimaryInvestor.objects._get_all_active_primary_investors_choices
    queryset = lambda x: []

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.get_choices()
        return super(PrimaryInvestorField, self).__init__(*args, **kwargs)

    def validate(self, value):
        pass
        #super(ChoiceField, self).validate(value)
        #if value and not self.valid_value(value):
        #    raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})

    def get_choices(self):
        #PrimaryInvestor.objects.update()
        return self.queryset()
