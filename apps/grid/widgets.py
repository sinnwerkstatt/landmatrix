"""
Collected form widgets
"""
import re

from django import forms
from django.forms import ClearableFileInput
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from file_resubmit.widgets import ResubmitFileWidget

from apps.landmatrix.models import Country
from apps.landmatrix.storage import data_source_storage
from apps.ol3_widgets.widgets import SerializedMapWidget


class TitleWidget(forms.TextInput):
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        return "<h3>%s</h3>" % str(self.initial or "")


class YearBasedWidget(forms.MultiWidget):
    year_based = True
    widget = forms.TextInput(attrs={"class": "year-based"})

    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        if "attrs" in kwargs:
            self.widget.attrs.update(kwargs.pop("attrs"))
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedWidget, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            self.widget,
            forms.TextInput(attrs={"class": "year-based-year"}),
            forms.CheckboxInput(attrs={"class": "year-based-is-current"}),
        ]

    def decompress(self, value):
        widgets = self.get_widgets()
        multiple = self.get_multiple()
        if value:
            values = []
            for i, val in enumerate(re.split("[#:]", value)):
                if multiple[i % len(widgets)]:
                    values.append(val.split(","))
                else:
                    values.append(val)
            return values
        return [None, None]

    def render_for_template(self):
        raise NotImplementedError()

    def format_output(self, rendered_widgets):
        return "".join(rendered_widgets)

    def get_multiple(self):
        # Check which widgets allow multiple values
        return [
            hasattr(w, "allow_multiple_selected") and w.allow_multiple_selected
            for w in self.get_widgets()
        ]

    def value_from_datadict(self, data, files, name):
        # Find out which widgets allow multiple values
        widgets = self.get_widgets()
        multiple = self.get_multiple()
        value = []
        # Grab last item and enumerate, since there can be gaps
        # because of checkboxes not submitting data
        keys = [
            int(k.replace(name + "_", ""))
            for k in data.keys()
            if re.match(name + "_\d", k)
        ]
        count = len(keys) > 0 and max(keys) + 1 or 0
        if count % len(widgets) > 0:
            count += 1
        for i in range(count):
            key = name + "_" + str(i)
            if multiple[i % len(widgets)]:
                value.append(data.getlist(key))
            else:
                value.append(data.get(key))
        # update widgets
        self.widgets = []
        for i in range(int(len(value) / len(widgets))):
            self.widgets.extend(widgets)
        return value

    def render(self, name, value, attrs=None, renderer=None):
        # update widgets
        if value:
            self.widgets = []
            value = isinstance(value, (list, tuple)) and value or self.decompress(value)
            for i in range(int(len(value) / len(self.get_widgets()))):
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
        id_ = final_attrs.get("id", None)
        helptext = (
            self.help_text
            and '<span class="helptext input-group-addon">%s</span>'
            % str(self.help_text)
            or ""
        )
        widgets_count = len(self.widgets)
        widgets_row_count = len(self.get_widgets())
        output.append('<div class="input-group">')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id="%s_%s" % (id_, i))
            # Append helptext before last widget (is current)
            if ((i + 1) % widgets_row_count) == 0:
                output.append(helptext)
            attrs = dict(final_attrs)
            attrs["class"] = " ".join(
                [
                    final_attrs.get("class", ""),
                    hasattr(widget, "attrs") and widget.attrs.get("class", "") or "",
                ]
            )
            output.append(
                widget.render(name + "_%s" % i, widget_value, attrs, renderer)
            )
            # Close reopen div every n element
            if ((i + 1) % widgets_row_count) == 0:
                # Add "Add more" button to first row
                if (i + 1) == widgets_row_count:
                    output.append(
                        '<a href="javascript:;" class="btn add-ybd add-row"><i class="lm lm-plus"></i> Add more</a>'
                    )
                    output.append(
                        '<a href="javascript:;" class="btn remove-ybd delete-row" style="display:none;"><i class="lm lm-minus"></i> Remove</a>'
                    )
                else:
                    output.append(
                        '<a href="javascript:;" class="btn remove-ybd delete-row"><i class="lm lm-minus"></i> Remove</a>'
                    )
                if (i + 1) < widgets_count:
                    output.append('</div><div class="input-group">')
        output.append("</div>")
        return mark_safe(self.format_output(output))


class YearBasedTextInput(YearBasedWidget):
    widget = None

    def __init__(self, *args, **kwargs):
        self.widget = forms.TextInput(attrs={"class": "year-based"})
        super().__init__(*args, **kwargs)

    def decompress(self, value):
        if value:
            splitted = []
            for s in value.split("#"):
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
        self.widget = forms.SelectMultiple(
            choices=self.choices, attrs={"class": "year-based"}
        )
        super(YearBasedSelectMultiple, self).__init__(*args, **kwargs)


class YearBasedSelectMultipleNumber(YearBasedWidget):
    placeholder = _("Size")

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        if "placeholder" in kwargs.get("attrs", {}):
            self.placeholder = kwargs["attrs"].pop("placeholder")
        super(YearBasedSelectMultipleNumber, self).__init__(*args, **kwargs)

    def get_widgets(self):
        widgets = [
            forms.SelectMultiple(choices=[], attrs={"class": "year-based"}),
            # Don't use NumberInput here, since it doesn't allow setSelectionRange (used by input filter JS)
            forms.TextInput(
                attrs={
                    "class": "year-based input-filter-number",
                    "placeholder": self.placeholder,
                }
            ),
            forms.TextInput(attrs={"class": "year-based-year"}),
            forms.CheckboxInput(attrs={"class": "year-based-is-current"}),
        ]
        # Prevent early database query fired by list(choices) method in widget init
        widgets[0].choices = self.choices
        return widgets


class TextChoiceInput(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(TextChoiceInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [forms.TextInput(), forms.Select(choices=self.choices)]


class MultiTextInput(YearBasedWidget):
    def get_widgets(self):
        return [forms.TextInput()]


class PrimaryInvestorSelect(forms.Select):
    def render(self, name, value, attrs=None, renderer=None):
        output = super(PrimaryInvestorSelect, self).render(name, value, attrs, renderer)
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
            "name": name,
        }
        return output


class NumberInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs.update({"type": "number", "class": "form-control input-filter-number"})
        return super(NumberInput, self).render(name, value, attrs, renderer)


class FileInputWithInitial(ResubmitFileWidget):
    displayed_chars = 40
    existing_file_template = (
        '<a class="input-group-addon" href="{url}" target="_blank" '
        'title="{label}" class="toggle-tooltip"><i class="fa fa-file-pdf-o"></i></a>'
    )
    new_upload_template = "{}-new"

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if attrs is None:  # pragma: no cover
            attrs = {}

        output = ""

        if value:
            if self.is_initial(value):
                # previously uploaded file
                value_name = str(value.name)
                value_url = value.url
            else:
                value_name = str(value)
                value_url = data_source_storage.url(value_name)

            if len(value_name) > self.displayed_chars:
                display_name = value_name[: self.displayed_chars] + "..."
            else:
                display_name = value_name

            output += self.existing_file_template.format(
                url=value_url, name=display_name, label=_("Current file")
            )

        file_input = super().render(
            self.new_upload_template.format(name), None, attrs, renderer, **kwargs
        )
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
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        has_id = attrs and "id" in attrs
        final_attrs = self.build_attrs(attrs, {name: name})
        output = ["<ul>"]
        # Normalize to strings
        str_values = set([force_str(v) for v in value])
        for i, (option_value, option_label, option_choices) in enumerate(self.choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id="%s_%s" % (attrs["id"], i))
                label_for = ' for="%s"' % final_attrs["id"]
            else:
                label_for = ""

            cb = forms.CheckboxInput(
                final_attrs, check_test=lambda value: value in str_values
            )
            option_value = force_str(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_str(option_label))
            option = "<li><label%s>%s %s</label>" % (
                label_for,
                rendered_cb,
                option_label,
            )
            if option_choices:
                option += "<ul>"
                for j, (option_value, option_label) in enumerate(option_choices):
                    if has_id:
                        final_attrs = dict(
                            final_attrs, id="%s_%s" % (attrs["id"], "%s-%s" % (i, j))
                        )
                        label_for = ' for="%s"' % final_attrs["id"]
                    else:
                        label_for = ""
                    cb = forms.CheckboxInput(
                        final_attrs, check_test=lambda value: value in str_values
                    )
                    option_value = force_str(option_value)
                    rendered_cb = cb.render(name, option_value)
                    option_label = conditional_escape(force_str(option_label))
                    option += "<li><label%s>%s %s</label></li>" % (
                        label_for,
                        rendered_cb,
                        option_label,
                    )

                option += "</ul>"
            option += "</li>"
            output.append(option)
        output.append("</ul>")
        return mark_safe("\n".join(output))


class CountrySelect(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        code = ""
        if value:
            if not isinstance(value, int):
                value = value.value
            code = Country.objects.defer("geom").get(pk=value).code_alpha2
        option["attrs"].update({"title": code})
        return option


class CommentInput(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        attrs.update({"rows": "3", "class": "form-control"})
        return super(CommentInput, self).render(name, value, attrs, renderer)


class AreaWidget(forms.MultiWidget):
    """
    Area widget includes a map, and a shapefile upload field.
    """

    MAP_WIDGET_ATTRS = {
        "map_width": 600,
        "map_height": 400,
        "initial_zoom": 8,
        "initial_center_lat": 0,
        "initial_center_lon": 0,
        "show_layer_switcher": True,
        "geom_type": "MULTIPOLYGON",
    }
    FILE_WIDGET_ATTRS = {"multiple": True}
    map_srid = 4326

    def __init__(self, *args, **kwargs):
        self.initially_hidden = kwargs.pop("initially_hidden", True)
        map_attrs = self.MAP_WIDGET_ATTRS.copy()
        map_attrs.update(kwargs.pop("map_attrs", {}))
        file_attrs = self.FILE_WIDGET_ATTRS.copy()
        file_attrs.update(kwargs.pop("file_attrs", {}))

        widgets = [
            SerializedMapWidget(attrs=map_attrs),
            # ResubmitFileWidget(attrs=file_attrs),  - doesn't yet seem to support multiple
            ClearableFileInput(attrs=file_attrs),
        ]
        super().__init__(widgets, *args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        """
        Overridden to pass name to format_output, so we can do js things
        with the map.
        """
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get("id", None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:  # pragma: no cover
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id="%s_%s" % (id_, i))
            output.append(
                widget.render(name + "_%s" % i, widget_value, final_attrs, renderer)
            )
        return mark_safe(self.format_output(name, output))

    def decompress(self, value):
        return [value, False]

    def format_output(self, name, rendered_widgets):
        if self.initially_hidden:
            container_style = "display: none;"
            show_hide_link_text = _("Show area")
            show_hide_link_alt_text = _("Hide area")
        else:
            container_style = ""
            show_hide_link_text = _("Hide area")
            show_hide_link_alt_text = _("Show area")

        output = """
        <div id="{name}-container" class="area-container" style="{style}">
            {map_widget}
            <div class="input-group">
                {file_widget}
                <div class="input-group-addon">{file_label}</div>
            </div>
        </div>
        <a href="#{name}-container" class="show-hide-area pull-right" data-alternate="{link_alt_text}">{link_text}</a>
        """.format(
            name=name,
            style=container_style,
            map_widget=rendered_widgets[0],
            file_widget=rendered_widgets[1],
            link_text=show_hide_link_text,
            link_alt_text=show_hide_link_alt_text,
            file_label=_(
                "Shapefile upload (select all files, required: .shp, .shx, .dbf, and .prj)"
            ),
        )

        return output


class InvestorSelect(forms.Select):
    """Custom select to add data attributes to options"""

    data = {}

    def __init__(self, *args, **kwargs):
        data = kwargs.pop("data", {})
        if data:
            self.data = data
        super(InvestorSelect, self).__init__(*args, **kwargs)

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        data_attributes = self.data.get(str(value), {})
        option["attrs"].update(
            dict(("data-%s" % d[0], d[1]) for d in data_attributes.items())
        )
        return option
