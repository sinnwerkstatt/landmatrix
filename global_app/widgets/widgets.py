from global_app.widgets.year_based_text_input import YearBasedTextInput

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'



from itertools import chain
import re

from django.utils.html import escape, conditional_escape
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from landmatrix.models import Country


from .number_input import NumberInput

class YearBasedIntegerField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.IntegerField(required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedTextInput(help_text=kwargs.pop("help_text", ""))
        super(YearBasedIntegerField, self).__init__(*args, **kwargs)

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
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]

class YearBasedCheckboxInput(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedCheckboxInput, self).__init__(*args, **kwargs)

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
        super(YearBasedBooleanField, self).__init__(*args, **kwargs)

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
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]

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

class CountryField(forms.ModelChoiceField):
    widget = CountrySelect(attrs={"readonly":"readonly"})

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Country.objects.all().order_by("name")
        super(CountryField, self).__init__(*args, **kwargs)

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
        super(PrimaryInvestorField, self).__init__(*args, **kwargs)

    def validate(self, value):
        pass
        #super(ChoiceField, self).validate(value)
        #if value and not self.valid_value(value):
        #    raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})

    def get_choices(self):
        #PrimaryInvestor.objects.update()
        return self.queryset()
