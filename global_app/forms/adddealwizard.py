import os, re

if False:
    import urllib2
if False:
    from django.utils import simplejson as json
if False:
    from wkhtmltopdf import wkhtmltopdf
if False:
    from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode

from global_app.widgets import *
from landmatrix.models import *

from copy import copy, deepcopy
from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.forms.models import formset_factory
from django.forms.formsets import BaseFormSet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile, File
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.utils.html import conditional_escape

from django.utils.safestring import mark_safe
from django.utils.dateformat import DateFormat
from django.utils.datastructures import MultiValueDict, SortedDict
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.formtools.wizard.forms import ManagementForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.uploadedfile import UploadedFile, SimpleUploadedFile



class BaseForm(forms.Form):
    error_css_class = "error"

    def as_ul(self):
        return self._html_output(
                    normal_row = u'<li%(html_class_attr)s>%(label)s <div class="input-append clearfix">%(field)s%(help_text)s</div>%(errors)s</li>',
                    error_row = u'<li>%s</li>',
                    row_ender = '</li>',
                    help_text_html = u' <span class="helptext add-on">%s</span>',
                    errors_on_separate_row = False)

    def as_table(self):
        return self._html_output(
            normal_row = '<tr%(html_class_attr)s"><th>%(label)s</th><td><div class="input-append clearfix">%(field)s%(help_text)s</div>%(errors)s</td></tr>',
            error_row = '<tr><td colspan="2">%s</td></tr>',
            row_ender = '</td></tr>',
            help_text_html = '<span class="helptext add-on">%s</span>',
            errors_on_separate_row = False)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes = ' '.join(["field", "control-group", name, css_classes])
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'name': name
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))

    def get_taggroups(self, request=None):
        """Create json for groups/tags/values from request"""
        # form data given?
        if self.data.get(self.prefix and "%s-TOTAL_FORMS"%self.prefix or "TOTAL_FORMS", 1) < 1:
            return []
        taggroups = []
        taggroup = {
            "main_tag": {
                "key": "name",
                "value": ""
            },
            "tags": [],
            "comment": ""
        }
        for i, (n, f) in enumerate(self.fields.items()):
            # New tag group?
            if n.startswith('tg_'):
                if n.endswith('_comment'):
                    comment = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n, None)
                    if comment:
                        taggroup["comment"] = comment
                else:
                    if taggroup["main_tag"]["value"] and (taggroup["tags"] or taggroup["comment"]):
                        taggroups.append(deepcopy(taggroup))
                    taggroup["main_tag"]["value"] = n[3:]
                    taggroup["tags"] = []
                    taggroup["comment"] = ""
            else:
                tag = {
                    "key": unicode(n)
                }
                if n == "investment_ratio":
                    taggroup["investment_ratio"] = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                # don't add choices for select fields, they're always the same
                elif isinstance(f, UserModelChoiceField):
                    value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n, [])
                    if value:
                        tag["value"] = value
                        taggroup["tags"].append(tag)
                elif isinstance(f, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)):
                    # Create tags for each value
                    tag["op"] = "select"
                    a = self.data
                    value = self.data.getlist(self.prefix and "%s-%s"%(self.prefix, n) or n, [])
                    for v in list(value):
                        if v:
                            v = int(v)
                            try:
                                tag["value"] = unicode(dict([i[:2] for i in f.choices])[v])
                            except:
                                tag["value"] = None
                            if isinstance(f, NestedMultipleChoiceField) and not tag["value"]:
                                for choice in f.choices:
                                    try:
                                        tag["value"] = unicode(dict([i[:2] for i in choice[2]])[v])
                                        if tag["value"]:
                                            break
                                    except:
                                        tag["value"] = None
                            if not tag["value"]:
                                tag["value"] = v
                            if tag["value"]:
                                taggroup["tags"].append(copy(tag))
                elif isinstance(f, forms.ChoiceField):
                    tag["op"] = "select"
                    value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
#                    if taggroup["main_tag"]["value"] == "investor":
#                        raise IOError, self.data
#                    if taggroup["main_tag"]["value"] == "investor" and value:
#                        raise IOError, n
                    # quickfix for receiving 'Non' as a value FIXME
                    if value and value != "0" and value != "Non":
                        if tag["key"] in ("investor", "primary_investor"):
                            tag["value"] = value
                            taggroup["tags"].append(tag)
                        else:
                            try:
                                tag["value"] = int(value)
                                tag["value"] = unicode(dict(f.choices).get(tag["value"]))
                                if tag["value"]:
                                    taggroup["tags"].append(tag)
                            except:
                                raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
                # Year based data?
                elif isinstance(f, forms.MultiValueField):
                    keys = filter(lambda o: re.match(r'%s_\d+'% (self.prefix and "%s-%s"%(self.prefix, n) or "%s"%n), o), self.data.keys())
                    keys.sort()
                    for i in range(len(keys)):
                        if i % 2 == 0:
                            value = self.data.get(len(keys) > i and keys[i] or "-", "")
                            year = self.data.get(len(keys) > i+1 and keys[i+1] or "-", "")
                            if value or year:
                                # allow zero value if yearbasedintegerfield
                                if value and (isinstance(f.fields[0], forms.IntegerField) or value != "0"):
                                    if isinstance(f.fields[0], forms.ChoiceField):
                                        try:
                                            tag["value"] = int(value)
                                            tag["value"] = unicode(dict(f.fields[0].choices).get(tag["value"]))
                                        except:
                                            raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
                                    else:
                                        tag["value"] = value
                                if year:
                                    tag["year"] = year
                                taggroup["tags"].append(tag)
                                tag = {
                                    "key": unicode(n)
                                }
                elif isinstance(f, forms.FileField):
                    tag["value"] = self.is_valid() and self.cleaned_data.get(n) and hasattr(self.cleaned_data.get(n), "name") and self.cleaned_data.get(n).name or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                    if tag["value"]:
                        taggroup["tags"].append(tag)
                elif isinstance(f, forms.DecimalField):
                    value = tag["value"] = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                    if value:
                        tag["value"] = str(value)
                        taggroup["tags"].append(tag)
                else:
                    tag["value"] = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                    if tag["value"]:
                        taggroup["tags"].append(tag)
            if i == len(self.fields.items())-1:
                if taggroup["main_tag"]["value"] and (taggroup["tags"] or taggroup["comment"]):
                    taggroups.append(deepcopy(taggroup))

        return taggroups

    def get_availability(self):
        available_field_count = 0.0
        if self.data.get(self.prefix and "%s-TOTAL_FORMS"%self.prefix or "TOTAL_FORMS", 1) < 1:
            return 0
        for i, (n, f) in enumerate(self.fields.items()):
            value, year = None, None
            if not n.startswith("tg_"):
                if isinstance(f, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)):
                    value = self.data.getlist(self.prefix and "%s-%s"%(self.prefix, n) or n, [])
                elif isinstance(f, forms.ChoiceField):
                    value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                    #filter default selection of choice fields
                    value = value != "0" and value or None
                    if value and isinstance(f.choices,(list, tuple)) and int(f.choices[0][0]) != 0:
                        value = None
                # Year based data?
                elif isinstance(f, forms.MultiValueField):
                    keys = filter(lambda o: re.match(r'%s_\d+'% (self.prefix and "%s-%s"%(self.prefix, n) or "%s"%n) ,o), self.data.keys())
                    keys.sort()
                    for i in range(len(keys)):
                        if i % 2 == 0:
                            value = self.data.get(len(keys) > i and keys[i] or "-", "")
                            if value == "0" and isinstance(f.fields[0], forms.ChoiceField):
                                #filter default selection of choice fields
                                value = None
                            year = self.data.get(len(keys) > i+1 and keys[i+1] or "-", "")
                            if value or year:
                                break
                elif isinstance(f, forms.FileField):
                    value = self.is_valid() and self.cleaned_data.get(n) and hasattr(self.cleaned_data.get(n), "name") and self.cleaned_data.get(n).name or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                else:
                    value = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
            if value or year:
                available_field_count = available_field_count + 1
        return available_field_count

    def get_availability_total(self):
        count = 0
        for n in self.fields:
            f = self.fields[n]
            if isinstance(f, TitleField) or isinstance(f.widget, CommentInput) or isinstance(f.widget, forms.HiddenInput) or "readonly" in f.widget.attrs:
                pass
            else:
                count = count + 1
        return count

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        """
        Get form data for activity or stakeholder,
        using taggroup only - if given (for formsets)
        """
        data = MultiValueDict()
        taggroup = tg
        for i, (n, f) in enumerate(cls().fields.items()):
            pn = prefix and "%s-%s"%(prefix, n) or n
            if n.startswith('tg_'):
                if n.endswith('_comment'):
                    if taggroup and taggroup.comment_set.count() > 0:
                        data[pn] = taggroup.comment_set.all().order_by("-timestamp")[0].comment
                elif not tg:
                    try:
                        if isinstance(object, Stakeholder):
                            taggroup = object.sh_tag_group_set.get(fk_sh_tag__fk_sh_value__value=n[3:])
                        else:
                            taggroup = object.a_tag_group_set.get(fk_a_tag__fk_a_value__value=n[3:])
                    except:
                        taggroup = None
                        continue
            else:
                if not taggroup:
                    continue
                if isinstance(taggroup, SH_Tag_Group):
                    tags = taggroup.sh_tag_set.filter(fk_sh_key__key=unicode(n))
                else:
                    tags = taggroup.a_tag_set.filter(fk_a_key__key=unicode(n))
                if len(tags) > 0:
                    if isinstance(f, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)):
                        values = []
                        if isinstance(taggroup, SH_Tag_Group):
                            tvalues = [t.fk_sh_value.value for t in tags]
                        else:
                            tvalues = [t.fk_a_value.value for t in tags]
                        for l in tvalues:
                            value = ""
                            for k, v in [i[:2] for i in f.choices]:
                                if v == l:
                                    value = unicode(k)
                                    break
                            if isinstance(f, NestedMultipleChoiceField) and not value:
                                for choice in f.choices:
                                    for k, v in [i[:2] for i in choice[2] or []]:
                                        if v == l:
                                            value = unicode(k)
                                            break
                            if value:
                                values.append(value)
                        data[pn] = values
                    else:
                        # Year based data?
                        if isinstance(f, forms.MultiValueField):
                            yb_data = []
                            for tag in tags:
                                if isinstance(taggroup, SH_Tag_Group):
                                    value = tag.fk_sh_value.value
                                    year = ""
                                else:
                                    value = tag.fk_a_value.value
                                    year = tag.fk_a_value.year
                                if isinstance(f.fields[0], forms.ChoiceField):
                                    for k, v in f.fields[0].choices:
                                        if v == value:
                                            value = unicode(k)
                                            break
                                if year or value:
                                    yb_data.append("%s:%s" % (value or "", year or ""))
                            data[pn] = "|".join(yb_data)
                        else:
                            a = tags.all()
                            if isinstance(taggroup, SH_Tag_Group):
                                value = tags[0].fk_sh_value.value
                            else:
                                value = tags[0].fk_a_value.value
                                year = tags[0].fk_a_value.year
                            if isinstance(f, forms.ChoiceField):
                                for k, v in f.choices:
                                    if v == value:
                                        value = unicode(k)
                                        break
                                data[pn] = value
                            elif isinstance(f, forms.DateField):
                                # reformat date values
                                try:
                                    data[pn] = datetime.strptime(value, "%Y-%m-%d").strftime("%d:%m:%Y")
                                except:
                                    # catch invalid date formats from import
                                    data[pn] = value
                            else:
                                data[pn] = value
        return data

    class Meta:
        exclude = ()
        fields = ()
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        if hasattr(self.Meta, "exclude"):
            for field in self.Meta.exclude:
                del self.fields[field]
        if hasattr(self.Meta, "fields") and self.Meta.fields:
            fields = SortedDict()
            for field in self.Meta.fields:
                fields[field] = self.fields[field]
            self.fields = fields
        if hasattr(self.Meta, "readonly_fields") and self.Meta.readonly_fields:
            for n in self.Meta.readonly_fields:
                f = self.fields[n]
                if isinstance(f.widget, forms.Select):
                    self.fields[n].widget.attrs["disabled"] = "disabled"
                else:
                    self.fields[n].widget.attrs["readonly"] = True


class BaseModelForm(forms.ModelForm):
    def as_ul(self):
        return self._html_output(
                    normal_row = u'<li%(html_class_attr)s>%(label)s <div class="input-append clearfix">%(field)s%(help_text)s</div>%(errors)s</li>',
                    error_row = u'<li>%s</li>',
                    row_ender = '</li>',
                    help_text_html = u' <span class="helptext add-on">%s</span>',
                    errors_on_separate_row = False)

    def as_table(self):
        return self._html_output(
            normal_row = '<tr%(html_class_attr)s"><th>%(label)s</th><td><div class="input-append clearfix">%(field)s%(help_text)s</div>%(errors)s</td></tr>',
            error_row = '<tr><td colspan="2">%s</td></tr>',
            row_ender = '</td></tr>',
            help_text_html = '<span class="helptext add-on">%s</span>',
            errors_on_separate_row = False)


    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes = ' '.join(["field", "control-group", name, css_classes])
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'name': name
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))


class DealSpatialForm(BaseForm):
    # Location
    tg_location = TitleField(required=False, label="", initial=_("Location"))
    level_of_accuracy = forms.TypedChoiceField(required=False, label=_("Level of accuracy"), choices=(
        (0, _("---------")),
        (10, _("Country")),
        (20, _("Approximate level")),
        (30, _("Exact location")),
        (40, _("Exact coordinates")),
    ), coerce=int)
    location = forms.CharField(required=False, label=_("Location"), widget=LocationWidget)
    point_lat = forms.CharField(required=False, label=_("Latitude"), widget=forms.TextInput, initial="")
    point_lon = forms.CharField(required=False, label=_("Longitude"), widget=forms.TextInput, initial="")
    target_country = CountryField(required=False, label=_("Target Country"))
    target_region = forms.ModelChoiceField(required=False, label=_("Target Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by("name"))
    tg_location_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

DealSpatialBaseFormSet = formset_factory(DealSpatialForm, extra=1)
class AddDealSpatialFormSet(DealSpatialBaseFormSet):
    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
        return ds_taggroups

    @classmethod
    def get_data(cls, activity):
        taggroups = activity.a_tag_group_set.filter(fk_a_tag__fk_a_value__value__contains="location").order_by("fk_a_tag__fk_a_value__value")
        data = []
        for i, taggroup in enumerate(taggroups):
            data.append(DealSpatialForm.get_data(activity, tg=taggroup))
        return data

class AddDealGeneralForm(BaseForm):
    # Land area
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(required=False, label=_("Intended size"), help_text=_("ha"), widget=NumberInput)
    contract_size = YearBasedIntegerField(required=False, label=_("Current size under contract (leased or purchased area)"), help_text=_("ha"), widget=NumberInput)
    production_size = YearBasedIntegerField(required=False, label=_("Current size in operation (production)"), help_text=_("ha"), widget=NumberInput)
    tg_land_area_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Intention of investment
    tg_intention = TitleField(required=False, label="", initial=_("Intention of investment"))
    intention = NestedMultipleChoiceField(required=False, label=_("Intention of the investment"), choices=(
        (10, _("Agriculture"), (
           (11, _("Biofuels")),
           (12, _("Food crops")),
           (13, _("Livestock")),
           (14, _("Non-food agricultural commodities")),
           (15, _("Agriunspecified")),
        )),
        (20, _("Forestry"), (
           (21, _("For wood and fibre")),
           (22, _("For carbon sequestration/REDD")),
           (23, _("Forestunspecified")),
        )),
        (30, _("Mining"), None),
        (40, _("Tourism"), None),
        (60, _("Industry"), None),
        (70, _("Conservation"), None),
        (80, _("Renewable Energy"), None),
        (90, _("Other (please specify)"), None),
    ))
    tg_intention_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Nature of the deal
    tg_nature = TitleField(required=False, label="", initial=_("Nature of the deal"))
    nature = forms.MultipleChoiceField(required=False, label=_("Nature of the deal"), choices=(
        (10, _("Outright Purchase")),
        (20, _("Lease / Concession")),
        (30, _("Exploitation license")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_nature_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Negotiation status,
    tg_negotiation_status = TitleField(required=False, label="", initial=_("Negotiation status"))
    negotiation_status = YearBasedChoiceField(required=False, label=_("Negotiation status"), choices=(
        (0, _("---------")),
        (30, _("Concluded (Oral Agreement)")),
        (40, _("Concluded (Contract signed)")),
        (10, _("Intended (Expression of interest)")),
        (20, _("Intended (Under negotiation)")),
        (50, _("Failed (Negotiations failed)")),
        (60, _("Failed (Contract canceled)")),
    ))
    contract_number = forms.IntegerField(required=False, label=_("Contract number"));
    contract_date = forms.DateField(required=False, label=_("Contract date"), help_text="[dd:mm:yyyy]", input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"])
    tg_negotiation_status_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Duration of the agreement
    tg_agreement_duration = TitleField(required=False, label="", initial=_("Duration of the agreement"))
    agreement_duration = YearBasedIntegerField(required=False, label=_("Duration of the agreement"), help_text=_("years"))
    # Implementation status
    tg_implementation_status = TitleField(required=False, label="", initial=_("Implementation status"))
    implementation_status = YearBasedChoiceField(required=False, label=_("Implementation status"), choices=(
        (0, _("---------")),
        (10, _("Project not started")),
        (20, _("Startup phase (no production)")),
        (30, _("In operation (production)")),
        (40, _("Project abandoned")),
    ))
    tg_implementation_status_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Purchase price
    tg_purchase_price = TitleField(required=False, label="", initial=_("Purchase price"))
    purchase_price = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Purchase price"))
    purchase_price_currency = forms.ModelChoiceField(required=False, label=_("Purchase price currency"), queryset=Currency.objects.all().order_by("ranking", "name"))
    purchase_price_type = forms.TypedChoiceField(required=False, label=_("Purchase price area type"), choices=(
        (0, _("---------")),
        (10, _("per ha")),
        (20, _("for specified area")),
    ), coerce=int)
    purchase_price_area = forms.IntegerField(required=False, label=_("Purchase price area"), help_text=_("ha"), widget=NumberInput)
    tg_purchase_price_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Leasing fees
    tg_leasing_fees = TitleField(required=False, label="", initial=_("Leasing fees"))
    annual_leasing_fee = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Annual leasing fee"))
    annual_leasing_fee_currency = forms.ModelChoiceField(required=False, label=_("Annual leasing fee currency"), queryset=Currency.objects.all().order_by("ranking", "name"))
    annual_leasing_fee_type = forms.TypedChoiceField(required=False, label=_("Annual leasing fee type"), choices=(
        (0, _("---------")),
        (10, _("per ha")),
        (20, _("for specified area")),
    ), coerce=int)
    annual_leasing_fee_area = forms.IntegerField(required=False, label=_("Purchase price area"), help_text=_("ha"), widget=NumberInput)
    tg_leasing_fees_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Contract farming
    tg_contract_farming = TitleField(required=False, label="", initial=_("Contract farming"))
    contract_farming = forms.ChoiceField(required=False, label=_("Contract farming"), choices=(
        (10, _("Yes")),
        (20, _("No")),
    ), widget=forms.RadioSelect)
    on_the_lease = forms.BooleanField(required=False, label=_("On leased / purchased area"))
    on_the_lease_area = forms.IntegerField(required=False, label=_("On leased / purchased area"), help_text=_("ha"), widget=NumberInput)
    on_the_lease_farmers = forms.IntegerField(required=False, label=_("On leased / purchased farmers"), help_text=_("farmers"), widget=NumberInput)
    off_the_lease = forms.BooleanField(required=False, label=_("Not on leased / purchased area (out-grower)"))
    off_the_lease_area = forms.IntegerField(required=False, label=_("Not on leased / purchased area (out-grower)"), help_text=_("ha"), widget=NumberInput)
    off_the_lease_farmers = forms.IntegerField(required=False, label=_("Not on leased / purchased farmers (out-grower)"), help_text=_("farmers"), widget=NumberInput)
    tg_contract_farming_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def clean_contract_date(self):
        date = self.cleaned_data["contract_date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(_("Invalid date. Please enter a date in the format [dd:mm:yyyy]"))


class AddDealEmploymentForm(BaseForm):
    # Total number of jobs created
    tg_total_number_of_jobs_created = TitleField(required=False, label="", initial=_("Number of total jobs created"))
    total_jobs_created = forms.BooleanField(required=False, label=_("Total number of jobs created"))
    total_jobs_planned = forms.IntegerField(required=False, label=_("Planned total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    total_jobs_current = YearBasedIntegerField(required=False, label=_("Current total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Current total employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    tg_total_number_of_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # Number of jobs for foreigners created
    tg_foreign_jobs_created = TitleField(required=False, label="", initial=_("Number of jobs for foreigners created"))
    foreign_jobs_created = forms.BooleanField(required=False, label=_("Number of jobs for foreigners created"))
    foreign_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of jobs for foreigners"), help_text=_("jobs"), widget=NumberInput)
    foreign_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    foreign_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    foreign_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of jobs for foreigners"), help_text=_("jobs"))
    foreign_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    foreign_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_foreign_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # Number of domestic jobs created
    tg_domestic_jobs_created = TitleField(required=False, label="", initial=_("Number of domestic jobs created"))
    domestic_jobs_created = forms.BooleanField(required=False, label=_("Number of domestic jobs created"))
    domestic_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of domestic jobs"), help_text=_("jobs"), widget=NumberInput)
    domestic_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    domestic_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    domestic_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of domestic jobs"), help_text=_("jobs"))
    domestic_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    domestic_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_domestic_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class ChangePrimaryInvestorForm(BaseForm):
    """
        used only in the change primary investor dialog and not in the wizard.
    """
    primary_investor_name = forms.CharField(required=True, label=_("Name of primary investor"), max_length=255)
    action_comment = forms.CharField(required=False, label=_("Action comment"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
            kwargs.pop("instance")
        super(ChangePrimaryInvestorForm, self).__init__(*args, **kwargs)

    def save(self):
        return self


class AddPrimaryInvestorForm(BaseForm):
    """
        used only in the add primary investor dialog and not in the wizard.
    """
    primary_investor_name = forms.CharField(required=True, label=_("Name of primary investor"), max_length=255)
    action_comment = forms.CharField(required=False, label=_("Action comment"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
            kwargs.pop("instance")
        super(AddPrimaryInvestorForm, self).__init__(*args, **kwargs)

    def clean_primary_investor_name(self):
        pi_name = self.cleaned_data["primary_investor_name"]
        pi = PrimaryInvestor.objects._get_active_primary_investor_by_name(pi_name)
        if pi_name and pi:
             raise forms.ValidationError(_("Primary investor name already exists. Please choose a different name."))
        return pi_name

    def save(self):
        return self


class DealPrimaryInvestorForm(BaseForm):
    tg_primary_investor = TitleField(required=False, label="", initial=_("Primary investor"))
    project_name = forms.CharField(required=False, label=_("Name of the investment project"), max_length=255)
    # TODO fix
    #primary_investor = forms.ChoiceField(required=False, label=_("Existing primary investor"), choices=PrimaryInvestor.objects._get_all_active_primary_investors_choices(), widget=PrimaryInvestorSelect)
    primary_investor = PrimaryInvestorField(required=False, label=_("Existing primary investor"))
    tg_primary_investor_comment = forms.CharField(required=False, label=_("Additional comments regarding investors"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        super(DealPrimaryInvestorForm, self).__init__(*args, **kwargs)
        self.fields["primary_investor"].choices = [("", str(_("---------"))),] + self.fields["primary_investor"].get_choices()


    def get_primary_investor(self):
        primary_investor = {
            "op": "add"
        }
        for j, taggroup in enumerate(super(DealPrimaryInvestorForm, self).get_taggroups()):
            # Existing primary investor?
            for t in taggroup["tags"]:
                if t["key"] == "primary_investor" and t["value"]:
                    primary_investor["op"] = "select"
                    primary_investor["id"] = t["value"]
                if t["key"] == "primary_investor_name":
                    primary_investor["name"] = t["value"]
        return primary_investor

    def get_taggroups(self, request=None):
        taggroups = super(DealPrimaryInvestorForm, self).get_taggroups()
        for tg in taggroups:
            tags = []
            for t in tg["tags"]:
                if t["key"] == "project_name":
                    tags.append(t)
            tg["tags"] = tags
        return taggroups

    @classmethod
    def get_data(cls, activity):
        data = super(DealPrimaryInvestorForm, cls).get_data(activity)
        primary_investor = primary_investor = PrimaryInvestor.objects.get_primary_investor_for_activity(activity)
        if primary_investor:
            data["primary_investor"] = primary_investor.primary_investor_identifier
        return data

    def get_availability(self):
        """
        Availability of investor form is 1 if a primary investor is defined
        """
        if self.data.get("primary_investor", None) or self.data.get("primary_investor_name", None):
            return 1
        return 0

    def get_availability_total(self):
        return 1

    def clean_primary_investor(self):
        pi_id = None
        if self.data.get("primary_investor"):
            pi_id = int(self.data.get("primary_investor", 0))
        choices = dict(self.fields["primary_investor"].choices).keys()
        if pi_id and pi_id not in choices:
            #self.fields["primary_investor"].choices.append([pi_id, pi_name])
            #c_old = self.fields["primary_investor"].choices
            #self.base_fields["primary_investor"].choices.append([pi_id, pi_name])
            choices = self.fields["primary_investor"].get_choices()
            self.fields["primary_investor"].choices = choices
            self.base_fields["primary_investor"].choices = choices
            #self.base_fields["primary_investor"].update_choices()

            #c_new = self.fields["primary_investor"].choices
        return self.cleaned_data

class DealSecondaryInvestorForm(BaseForm):
    # Investor
    tg_investor = TitleField(required=False, label="", initial=_("Investor"))
    investor = forms.ChoiceField(required=False, label=_("Existing investor"), choices=(), widget=LivesearchSelect)
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    region = forms.ModelChoiceField(required=False, label=_("Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by('name'))
    classification = forms.ChoiceField(required=False, label=_("Classification"), choices=(
        (10, _("Private company")),
        (20, _("Stock-exchange listed company")),
        (30, _("Individual entrepreneur")),
        (40, _("Investment fund")),
        (50, _("Semi state-owned company")),
        (60, _("State-/government(-owned)")),
        (70, _("Other (please specify in comment field)")),
    ), widget=forms.RadioSelect)
    investment_ratio = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%"))
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        investor = kwargs.pop("investor", None)
        super(DealSecondaryInvestorForm, self).__init__(*args, **kwargs)
        self.fields["investor"].initial = investor
        # TODO: fix
        #self.investor_choices = Stakeholder.objects.raw_choices()
        self.investor_choices = []
        self.fields["investor"].choices = list(self.fields["investor"].choices)[:1]
        self.fields["investor"].choices.extend([(s.id, s) for s in self.investor_choices])
        self.fields["country"].choices = [
            ("", str(_("---------"))),
            (0, str(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])

    def clean_investor(self):
        investor = int(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s.id for s in self.investor_choices]):
             raise forms.ValidationError("%s is no valid investor." % investor)
        return investor

    def clean(self):
        cleaned_data = super(DealSecondaryInvestorForm, self).clean()
        investor = cleaned_data.get("investor", None)
        investor_name = cleaned_data.get("investor_name", None)
        if not investor and not investor_name:
            raise forms.ValidationError("Please select an investor or investor name.")
        return cleaned_data

    def has_investor(self):
        if self.initial.has_key("investor") and self.initial["investor"]:
            return True
        elif self.is_valid() and self.cleaned_data.has_key("investor") and self.cleaned_data["investor"]:
            return True
        return False

BaseDealSecondaryInvestorFormSet = formset_factory(DealSecondaryInvestorForm, extra=0)
class DealSecondaryInvestorFormSet(BaseDealSecondaryInvestorFormSet):
    def get_taggroups(self, request=None):
        return []

    def get_stakeholders(self):
        stakeholders = []
        for i, form in enumerate(self.forms):
            stakeholder = {}
            for j, taggroup in enumerate(form.get_taggroups()):
                comment = taggroup.get("comment", "")
                for i, t in reversed(list(enumerate(taggroup["tags"]))):
                    if t["key"] == "investor":
                        # Existing investor
                        stakeholder["investment_ratio"] = unicode(taggroup["investment_ratio"])
                        stakeholder["id"] = t["value"]
                        stakeholder["taggroups"] = [{
                            "main_tag": {"key": "name", "value": "General"},
                            "comment": comment,
                        }]
                if not stakeholder:
                    stakeholder["investment_ratio"] = taggroup["investment_ratio"]
                    stakeholder["taggroups"] = [{
                        "main_tag": {"key": "name", "value": "General"},
                        "tags": taggroup["tags"],
                        "comment": comment,
                    }]
            if stakeholder:
                stakeholders.append(copy(stakeholder))
        return stakeholders

    @classmethod
    def get_data(cls, activity):
        #raise IOError, [{"investor": unicode(i.fk_stakeholder.id)} for i in activity.involvement_set.all()]
        data = []
        for i in activity.involvement_set.get_involvements_for_activity(activity):
            if not i.fk_stakeholder:
                continue
            comments = Comment.objects.filter(fk_sh_tag_group__fk_stakeholder=i.fk_stakeholder.id, fk_sh_tag_group__fk_sh_tag__fk_sh_value__value="General", fk_sh_tag_group__fk_sh_tag__fk_sh_key__key="name").order_by("-id")
            comment = ""
            if comments and len(comments) > 0:
                comment = comments[0].comment
            investor = {
                "investor": i.fk_stakeholder.id,
                "tg_general_comment": comment,
                "investment_ratio": i.investment_ratio,
            }
            data.append(investor)
        return data


class FileInputWithInitial(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super(FileInputWithInitial, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        output = []
        if value:
            value = isinstance(value, UploadedFile) and value.name or value
            output.append("<dl>")
            output.append("<dt>%s:</dt>" % unicode(_("Saved file")))
            output.append("<dd>")
            output.append('<a href="/media/uploads/%s" target="_blank"> %s</a>' % (value, value[:25]))
            output.append('<input type="hidden" name="%s" value="%s">' % (name, value))
            output.append("</dd>")
            output.append("</dl>")
        output.append(super(FileInputWithInitial, self).render("%s-new"%name, value, attrs))
        return "\n".join(output)

    def value_from_datadict(self, data, files, name):
        # New file uploaded?
        new_file = files.get("%s-new"%name)
        if new_file:
            return new_file
        value = data.get(name)
        if value:
            return SimpleUploadedFile(name=value, content=b'test')
        return ""

class FileFieldWithInitial(forms.FileField):
    widget = FileInputWithInitial
    show_hidden_initial = True

    def __init__(self, *args, **kwargs):
        #self.widget = FileInputWithInitial()
        super(FileFieldWithInitial, self).__init__(*args, **kwargs)

class DealDataSourceForm(BaseForm):
    # Data source
    tg_data_source = TitleField(required=False, label="", initial=_("Data source"))
    type = forms.TypedChoiceField(required=False, label=_("Data source type"), choices=(
        (10, _("Media report")),
        (20, _("Research Paper / Policy Report")),
        (30, _("Government sources")),
        (40, _("Company sources")),
        (50, _("Contract")),
        (60, _("Personal information")),
        (70, _("Crowdsourcing")),
        (80, _("Other (Please specify in comment  field)")),
    ), coerce=int)
    url = forms.URLField(required=False, label=_("New URL"), help_text=_("PDF will be generated automatically, leave empty for file upload"))
    file = FileFieldWithInitial(required=False, label=_("New file"))
    date = forms.DateField(required=False, label=_("Date"), help_text="[dd:mm:yyyy]", input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"])
    # Optional personal information for Crowdsourcing and Personal information
    name = forms.CharField(required=False, label=_("Name"))
    company = forms.CharField(required=False, label=_("Organisation"))
    email = forms.CharField(required=False, label=_("Email"))
    phone = forms.CharField(required=False, label=_("Phone"))
    includes_in_country_verified_information = forms.BooleanField(required=False, label=_("Includes in-country-verified information"))
    tg_data_source_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def clean_date(self):
        date = self.cleaned_data["date"]
        try:
            return date and date.strftime("%Y-%m-%d") or ""
        except:
            raise forms.ValidationError(_("Invalid date. Please enter a date in the format [dd:mm:yyyy]"))

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file and isinstance(file, File):
            n = file.name.split(".")
            # cleanup special charachters in filename
            file.name = "%s.%s" % (slugify(n[0]), n[1]) if len(n)>1 else slugify(n[0])
        return file

    def get_availability_total(self):
        return 4

    def __init__(self, *args, **kwargs):
        super(DealDataSourceForm, self).__init__(*args, **kwargs)



DealDataSourceBaseFormSet = formset_factory(DealDataSourceForm, extra=1)
class AddDealDataSourceFormSet(DealDataSourceBaseFormSet):
    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
                ds_url, ds_file = None, None
                for t in taggroup["tags"]:
                    if t["key"] == "url":
                        ds_url = t["value"]
                    elif t["key"] == "file":
                        ds_file = t["value"]
                #if ds_file:
                #    taggroup["tags"].append({
                #            "key": "file",
                #            "value": ds_file,
                #        })
                if ds_url:
                    url_slug = "%s.pdf" % re.sub(r"http|https|ftp|www|", "", slugify(ds_url))
                    if not ds_file or url_slug != ds_file:
                        # Remove file from taggroup
                        taggroup["tags"] = filter(lambda o: o["key"] != "file", taggroup["tags"])
                        # Create file for URL
                        if not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                            try:
                                # Check if URL changed and no file given
                                if ds_url.endswith(".pdf"):
                                    response = urllib2.urlopen(ds_url)
                                    default_storage.save("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug), ContentFile(response.read()))
                                else:
                                    # Create PDF from URL
                                    wkhtmltopdf(ds_url, "%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug))
                                # Set file tag
                            except:
                                # skip possible html to pdf conversion errors
                                if request and not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                                    messages.error(request, "Data source <a target='_blank' href='%s'>URL</a> could not be uploaded as a PDF file. Please upload manually." % ds_url)
                        taggroup["tags"].append({
                            "key": "file",
                            "value": url_slug,
                        })
                        # always add url, cause there is a problem with storing the file when deal get changed again
                        #taggroup["tags"].append({
                        #    "key": "url",
                        #    "value": ds_url,
                        #})
        return ds_taggroups

    @classmethod
    def get_data(cls, activity):
        taggroups = activity.a_tag_group_set.filter(fk_a_tag__fk_a_value__value__contains="data_source").order_by("fk_a_tag__fk_a_value__value")
        data = []
        for i, taggroup in enumerate(taggroups):
            data.append(DealDataSourceForm.get_data(activity, tg=taggroup))
        return data

class DealLocalCommunitiesForm(BaseForm):
    # How did community react?
    tg_community_reaction = TitleField(required=False, label="", initial=_("How did community react?"))
    community_reaction = forms.ChoiceField(required=False, label=_("Community reaction"), choices=(
        (10, _("Consent")),
        (20, _("Mixed reaction")),
        (30, _("Rejection")),
    ), widget=forms.RadioSelect)
    tg_community_reaction_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Consultation of local community
    tg_community_consultation = TitleField(required=False, label="", initial=_("Consultation of local community"))
    community_consultation = forms.ChoiceField(required=False, label=_("Community consultation"), choices=(
        (10, _("Not consulted")),
        (20, _("Limited consultation")),
        (30, _("Free prior and informed consent")),
        (40, _("Other")),
    ), widget=forms.RadioSelect)
    tg_community_consultation_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Promised or received compensation
    tg_community_compensation = TitleField(required=False, label="", initial=_("Promised or received compensation"))
    community_compensation = forms.CharField(required=False, label=_("Community compensation"), widget=CommentInput)
    # Benefits for local communities
    tg_community_benefits = TitleField(required=False, label="", initial=_("Benefits for local communities"))
    community_benefits = forms.MultipleChoiceField(required=False, label=_("Community benefits"), choices=(
        (10, _("Health")),
        (20, _("Education")),
        (30, _("Productive infrastructure (e.g. irrigation, tractors, machinery...)")),
        (40, _("Roads")),
        (50, _("Capacity Building")),
        (60, _("Financial Support")),
        (70, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_community_benefits_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Number of people actually displaced
    tg_number_of_displaced_people = TitleField(required=False, label="", initial=_("Number of people actually displaced"))
    number_of_displaced_people = forms.IntegerField(required=False, label=_("Number of displaced people"), help_text="", widget=NumberInput)
    tg_number_of_displaced_people_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class DealFormerUseForm(BaseForm):
    # Former land owner
    tg_land_owner = TitleField(required=False, label="", initial=_("Former land owner"))
    land_owner = forms.MultipleChoiceField(required=False, label=_("Former land owner"), choices=(
        (10, _("State")),
        (20, _("Private (smallholders)")),
        (30, _("Private (large-scale)")),
        (40, _("Community")),
        (50, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_owner_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Former land use
    tg_land_use = TitleField(required=False, label="", initial=_("Former land use"))
    land_use = forms.MultipleChoiceField(required=False, label=_("Former land use"), choices=(
        (10, _("Commercial (large-scale) agriculture")),
        (20, _("Smallholder agriculture")),
        (30, _("Pastoralists")),
        (40, _("Forestry")),
        (50, _("Conservation")),
        (60, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_use_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Former land cover
    tg_land_cover = TitleField(required=False, label="", initial=_("Former land cover"))
    land_cover = forms.MultipleChoiceField(required=False, label=_("Former land cover"), choices=(
        (10, _("Cropland")),
        (20, _("Forest land")),
        (30, _("Shrub land/Grassland")),
        (40, _("Marginal land")),
        (50, _("Other land")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_cover_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class DealProduceInfoForm(BaseForm):
    # Detailed crop, animal and mineral information
    tg_crop_animal_mineral = TitleField(required=False, label="", initial=_("Detailed crop, animal and mineral information"))
    crops = forms.ModelMultipleChoiceField(required=False, label=_("Crops"), queryset=Crop.objects.all(), widget=forms.CheckboxSelectMultiple)
    animals = forms.ModelMultipleChoiceField(required=False, label=_("Animals"), queryset=Animal.objects.all(), widget=forms.CheckboxSelectMultiple)
    minerals = forms.ModelMultipleChoiceField(required=False, label=_("Minerals"), queryset=Mineral.objects.all(), widget=forms.CheckboxSelectMultiple)

    # Use of produce
    tg_use_of_produce = TitleField(required=False, label="", initial=_("Use of produce"))
    has_domestic_use = forms.BooleanField(required=False, label=_("Has domestic use"))
    domestic_use = forms.IntegerField(required=False, label=_("Domestic use"), help_text=_("%"), widget=NumberInput)
    has_export = forms.BooleanField(required=False, label=_("Has export"))
    export = forms.IntegerField(required=False, label=_("Export"), help_text=_("%"), widget=NumberInput)
    export_country1 = forms.ModelChoiceField(required=False, label=_("Country 1"), queryset=Country.objects.all().order_by("name"))
    export_country1_ratio = forms.IntegerField(required=False, label=_("Country 1 ratio"), help_text=_("%"), widget=NumberInput)
    export_country2 = forms.ModelChoiceField(required=False, label=_("Country 2"), queryset=Country.objects.all().order_by("name"))
    export_country2_ratio = forms.IntegerField(required=False, label=_("Country 2 ratio"), help_text=_("%"), widget=NumberInput)
    export_country3 = forms.ModelChoiceField(required=False, label=_("Country 3"), queryset=Country.objects.all().order_by("name"))
    export_country3_ratio = forms.IntegerField(required=False, label=_("Country 3 ratio"), help_text=_("%"), widget=NumberInput)
    tg_use_of_produce_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # In-country processing of produce
    tg_in_country_processing = TitleField(required=False, label="", initial=_("In country processing of produce"))
    in_country_processing = forms.ChoiceField(required=False, label=_("In country processing of produce"), choices=(
        (10, _("Yes")),
        (20, _("No")),
    ), widget=forms.RadioSelect)
    tg_in_country_processing_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class DealWaterForm(BaseForm):
    # Water extraction envisaged
    tg_water_extraction_envisaged = TitleField(required=False, label="", initial=_("Water extraction envisaged"))
    water_extraction_envisaged = forms.ChoiceField(required=False, label=_("Water extraction envisaged"), choices=(
        (10, _("Yes")),
        (20, _("No")),
    ), widget=forms.RadioSelect)
    tg_water_extraction_envisaged_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Source of water extraction
    tg_source_of_water_extraction = TitleField(required=False, label="", initial=_("Source of water extraction"))
    source_of_water_extraction = NestedMultipleChoiceField(required=False, label=_("Source of water extraction"), choices=(
        (10, _("Groundwater"), None),
        (20, _("Surface water"), (
           (21, _("River")),
           (22, _("Lake")),
        )),
    ))
    tg_source_of_water_extraction_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # How much do investors pay for water and the use of water infrastructure?
    tg_how_much_do_investors_pay = TitleField(required=False, label="", initial=_("How much do investors pay for water and the use of water infrastructure?"))
    tg_how_much_do_investors_pay_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # How much water is extracted?
    tg_water_extraction_amount = TitleField(required=False, label="", initial=_("How much water is extracted?"))
    water_extraction_amount = forms.IntegerField(required=False, label=_("Water extraction amount"), help_text=mark_safe(_("m&sup3;/year")), widget=NumberInput)
    tg_water_extraction_amount_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class DealGenderRelatedInfoForm(BaseForm):
    # Any gender-specific information about the investment and its impacts
    tg_gender_specific_info = TitleField(required=False, label="", initial=_("Any gender-specific information about the investment and its impacts"))
    tg_gender_specific_info_comment = forms.CharField(required=False, label="", widget=CommentInput)



class AddDealActionCommentForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)
    fully_updated = forms.BooleanField(required=False, label=_("Fully updated"))
    fully_updated_history = forms.CharField(required=False, label=_("Fully updated history"), widget=forms.Textarea(attrs={"readonly":True, "cols": 80, "rows": 5}))


    tg_not_public = TitleField(required=False, label="", initial=_("Public deal"))
    not_public = forms.BooleanField(required=False, label=_("Not public"), help_text=_("Please specify in additional comment field"))
    not_public_reason = forms.ChoiceField(required=False, label=_("Reason"), choices=(
        (0, _("---------")),
        (10, _("Temporary removal from PI after criticism")),
        (20, _("Research in progress")),
    ))
    tg_not_public_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_feedback = TitleField(required=False, label="", initial=_("Feedback"))
    assign_to_user = UserModelChoiceField(required=False, label=_("Assign to"), queryset=User.objects.filter(groups__name__in=("Research admins", "Research assistants")).order_by("username"), empty_label=_("Unassigned"))
    tg_feedback_comment = forms.CharField(required=False, label=_("Feedback comment"), widget=CommentInput)

    def get_action_comment(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                return taggroup["comment"]
        return ""

    def get_feedback(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "feedback":
                tags = taggroup.get("tags", [])
                if len(tags) > 0:
                    feedback = {
                        "assigned_to": tags[0].get("value"),
                        "comment": taggroup.get("comment")
                    }
                    return feedback
        return ""

    def get_fully_updated(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                for tag in taggroup.get("tags", []):
                    if tag.get("key") == "fully_updated":
                        return tag.get("value")
        return False

    def get_taggroups(self, request=None):
        taggroups = []
        for tg in super(AddDealActionCommentForm, self).get_taggroups():
            if tg["main_tag"]["value"] in ("action", "feedback"):
                continue
            else:
                taggroups.append(tg)
        return taggroups

    @classmethod
    def get_data(cls, activity):
        data = super(AddDealActionCommentForm, cls).get_data(activity)
        a_feedback = A_Feedback.objects.filter(fk_activity=activity)
        if len(a_feedback) > 0:
            feedback = a_feedback[0]
            data.update({
                "assign_to_user": feedback.fk_user_assigned.id,
                "tg_feedback_comment": feedback.comment,
            })
        fully_updated_history = Activity.objects.get_fully_updated_history(activity.activity_identifier)
        fully_updated = []
        for h in fully_updated_history:
            fully_updated.append("%s - %s: %s" %(DateFormat(h.fully_updated).format("Y-m-d H:i:s"), h.username, h.comment))
        data.update({
            "fully_updated_history": "\n".join(fully_updated)
        })
        return data


class AddDealOverallCommentForm(BaseForm):
    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(required=False, label="", widget=CommentInput)

class AddInvestorForm(BaseForm):
    tg_general = TitleField(required=False, label="", initial=_("General"))
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    classification = forms.ChoiceField(required=False, label=_("Classification"), choices=(
        (10, _("Private company")),
        (20, _("Stock-exchange listed company")),
        (30, _("Individual entrepreneur")),
        (40, _("Investment fund")),
        (50, _("Semi state-owned company")),
        (60, _("State-/government(-owned)")),
        (70, _("Other (please specify in comment field)")),
    ), widget=forms.RadioSelect)
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
            kwargs["initial"] = self.get_data(kwargs.pop("instance"))
        super(AddInvestorForm, self).__init__(*args, **kwargs)
        self.fields["country"].choices = [
            ("", unicode(_("---------"))),
            (0, unicode(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])

    def save(self):
        return self

    def clean_investor(self):
        investor = long(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s.id for s in self.investor_choices]):
             raise forms.ValidationError("%s is no valid investor." % investor)
        return investor

    def get_taggroups(self, request=None):
        taggroups = super(AddInvestorForm, self).get_taggroups()
        return taggroups

class ManageDealForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
            kwargs.pop("instance")
        super(ManageDealForm, self).__init__(*args, **kwargs)

    def save(self):
        return self
