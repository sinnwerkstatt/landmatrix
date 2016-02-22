from global_app.widgets.nested_multiple_choice_field import NestedMultipleChoiceField
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.comment import Comment
from landmatrix.models.deal import Deal

from django.utils.datastructures import SortedDict, MultiValueDict
from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from copy import copy, deepcopy
import re

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class BaseForm(forms.Form):

    DEBUG = False

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
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_text(e)) for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes = ' '.join(["field", "control-group", name, css_classes])
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': str(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'name': name
                })

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

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
                    "key": str(n)
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
                                tag["value"] = str(dict([i[:2] for i in f.choices])[v])
                            except:
                                tag["value"] = None
                            if isinstance(f, NestedMultipleChoiceField) and not tag["value"]:
                                for choice in f.choices:
                                    try:
                                        tag["value"] = str(dict([i[:2] for i in choice[2]])[v])
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
                                tag["value"] = str(dict(f.choices).get(tag["value"]))
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
                                            tag["value"] = str(dict(f.fields[0].choices).get(tag["value"]))
                                        except:
                                            raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
                                    else:
                                        tag["value"] = value
                                if year:
                                    tag["year"] = year
                                taggroup["tags"].append(tag)
                                tag = {
                                    "key": str(n)
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
    def get_data(cls, deal, taggroup=None, prefix=""):
        """
        Get form data for activity or stakeholder,
        using taggroup only - if given (for formsets)
        """
        data = MultiValueDict()
        if cls.DEBUG: print('get_data', str(deal)[:140], '...', taggroup)
        for (field_name, field) in cls().fields.items():
            prefixed_name = prefix and "%s-%s"%(prefix, field_name) or field_name

            if cls.DEBUG: print('    field', field_name, field, prefix)

            if field_name.startswith('tg_'):
                taggroup = cls.get_data_for_tg_field(data, field_name, deal, prefixed_name, taggroup)

            else:
                tags, taggroup = cls.get_tags(field_name, deal, taggroup)

                if tags and len(tags) > 0:
                    if isinstance(field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)):
                        cls.get_multiple_choice_data(data, field, field_name, prefixed_name, taggroup)
                    else:
                        # Year based data?
                        if isinstance(field, forms.MultiValueField):
                            cls.get_year_based_data(data, field, field_name, prefixed_name, tags, taggroup)
                        else:
                            cls.get_other_data(data, field, field_name, prefixed_name, taggroup, tags)
        if cls.DEBUG: print('returned data', data)
        return data

    @classmethod
    def get_other_data(cls, data, field, field_name, prefixed_name, taggroup, tags):
        if cls.DEBUG: print('get_other_data')
        if isinstance(taggroup, ActivityAttributeGroup) and taggroup.attributes.get(field_name):
            value = taggroup.attributes[field_name]
        elif hasattr(taggroup, field_name):
            value = getattr(taggroup, field_name)
        elif field_name in tags:
            value = tags[field_name]
        else:
            if cls.DEBUG: print('didnt find %s' % field_name)
            value = None
        date = tags['date'] if 'date' in tags else None # tags.date or taggroup.date
        if cls.DEBUG: print('        value, date', value, date)

        if isinstance(field, forms.ChoiceField):
            for k, v in field.choices:
                if v == value:
                    value = str(k)
                    break
            data[prefixed_name] = value
        elif isinstance(field, forms.DateField):
            # reformat date values
            try:
                data[prefixed_name] = datetime.strptime(value, "%Y-%m-%d").strftime("%d:%m:%Y")
            except:
                # catch invalid date formats from import
                data[prefixed_name] = value
        else:
            data[prefixed_name] = value

    @classmethod
    def get_multiple_choice_data(cls, data, field, field_name, prefixed_name, taggroup):
        tag_values = set([group.attributes[field_name] for group in taggroup if field_name in group.attributes])
        if cls.DEBUG: print('get_multiple_choice_data()', field_name, list(field.choices), tag_values)
        values = []
        for tag_value in tag_values:
            value = cls.get_multiple_choice_value(field, tag_value)
            if value:
                values.append(value)
        data[prefixed_name] = values

    @classmethod
    def get_multiple_choice_value(cls, field, tag_value):
        value = cls.get_choice_value(field, tag_value)
        if isinstance(field, NestedMultipleChoiceField) and not value:
            value = cls.get_nested_choice_value(field, tag_value)
        return value

    @classmethod
    def get_nested_choice_value(cls, field, tag_value):
        for choice in field.choices:
            for k, v in [i[:2] for i in choice[2] or []]:
                if v == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                    return str(k)
        return None

    @classmethod
    def get_choice_value(cls, field, tag_value):
        for k, v in [i[:2] for i in field.choices]:
            if v == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                return str(k)
        return None

    @classmethod
    def get_year_based_data(cls, data, field, field_name, prefixed_name, tags, taggroup):
        if cls.DEBUG: print('get_year_based_data()', field_name, tags.get(field_name))
        yb_data = []

        for tag in [field_name]:
            value = tags.get(tag)
            year = tags.get('date', '')
            if isinstance(field.fields[0], forms.ChoiceField):
                for k, v in field.fields[0].choices:
                    if v == value:
                        value = str(k)
                        break
            if year or value:
                yb_data.append("%s:%s" % (value or "", year or ""))
        data[prefixed_name] = "|".join(yb_data)

    @classmethod
    def get_tags(cls, field_name, deal, taggroup):
        if not deal and not taggroup:
            return [], None

        if isinstance(deal, Deal):
            tags = deal.attributes
            if not taggroup:
                taggroup = list(deal.attribute_groups())
        # elif isinstance(taggroup, SH_Tag_Group):
        #     tags = taggroup.sh_tag_set.filter(fk_sh_key__key=str(field_name))
        elif taggroup is None:
            return None, None
        else:
            tags = taggroup.a_tag_set.filter(fk_a_key__key=str(field_name))
        return tags, taggroup

    @classmethod
    def get_data_for_tg_field(cls, data, field_name, deal, pn, taggroup):

        if field_name.endswith('_comment'):

            groups = taggroup if isinstance(taggroup, list) else [taggroup]
            comments = BaseForm.get_comments_from_taggroups(groups)
            cls.fill_comment_field(comments, data, field_name, pn)

        elif not taggroup:
            try:
                if isinstance(deal, Stakeholder):
                    taggroup = deal.sh_tag_group_set.get(fk_sh_tag__fk_sh_value__value=field_name[3:])
                else:
                    taggroup = deal.a_tag_group_set.get(fk_a_tag__fk_a_value__value=field_name[3:])
            except:
                taggroup = None
        return taggroup

    @classmethod
    def fill_comment_field(cls, comments, data, field_name, pn):
        if comments and field_name[3:] in comments:
            data[pn] = comments[field_name[3:]]

    @classmethod
    def get_comments_from_taggroups(cls, groups):
        return dict([(k, v) for group in [g for g in groups if g] for (k, v) in group.attributes.items() if '_comment' in k])

    class Meta:
        exclude = ()
        fields = ()
        readonly_fields = ()

    def __init__(self, *args, **kwargs):

        super(BaseForm, self).__init__(*args, **kwargs)
        if self.DEBUG:
            print(self.__class__.__name__, args)
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

