from copy import copy, deepcopy
import re

from django.utils.datastructures import SortedDict, MultiValueDict
from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

#from crispy_forms.helper import FormHelper

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.comment import Comment
from landmatrix.models.deal import Deal
from grid.widgets.nested_multiple_choice_field import NestedMultipleChoiceField


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class BaseForm(forms.Form):
    DEBUG = False
    error_css_class = "error"

    def get_attributes(self, request=None):
        """Create json for attributes from request"""
        # form data given?
        if self.data.get(self.prefix and "%s-TOTAL_FORMS"%self.prefix or "TOTAL_FORMS", 1) < 1:
            return {}
        attributes = {}
        for i, (n, f) in enumerate(self.fields.items()):
            key = key = str(n)
            # New tag group?
            if n.startswith('tg_'):
                if n.endswith('_comment'):
                    key = 'comment'
                else:
                    continue
                #if n.endswith('_comment'):
                    #raise NotImplementedError('Comment')
                    #comment = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n, None)
                    #if comment:
                    #    activity["comment"] = comment
                #else:
                    #if activity["main_tag"]["value"] and (attributes or activity["comment"]):
                    #    attributes.append(deepcopy(activity))
                    #activity["main_tag"]["value"] = n[3:]
                    #attributes = []
                    #activity["comment"] = ""
            #if n == "investment_ratio":
            #    activity["investment_ratio"] = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
            # don't add choices for select fields, they're always the same
            #elif isinstance(f, UserModelChoiceField):
            #    value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n, [])
            #    if value:
            #        tag["value"] = value
            #        attributes.append(tag)
            if isinstance(f, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)):
                # Create tags for each value
                #tag["op"] = "select"
                a = self.data
                value = self.data.getlist(self.prefix and "%s-%s"%(self.prefix, n) or n, [])
                for v in list(value):
                    if v:
                        v = int(v)
                        try:
                            value = str(dict([i[:2] for i in f.choices])[v])
                        except:
                            value = None
                        if isinstance(f, NestedMultipleChoiceField) and not value:
                            for choice in f.choices:
                                try:
                                    value = str(dict([i[:2] for i in choice[2]])[v])
                                    if value:
                                        break
                                except:
                                    value = None
                        if not value:
                            value = v
                        if value:
                            attributes[key] = value
            elif isinstance(f, forms.ChoiceField):
                #tag["op"] = "select"
                value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
#                if activity["main_tag"]["value"] == "investor":
#                    raise IOError, self.data
#                if activity["main_tag"]["value"] == "investor" and value:
#                    raise IOError, n
                # quickfix for receiving 'Non' as a value FIXME
                if value and value != "0" and value != "Non":
                    if key in ("investor", "primary_investor"):
                        attributes[key] = value
                    else:
                        try:
                            value = int(value)
                            value = str(dict(f.choices).get(value))
                            if value:
                                attributes[key] = value
                        except:
                            raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
            # Year based data?
            elif isinstance(f, forms.MultiValueField):
                keys = list(filter(lambda o: re.match(r'%s_\d+'% (self.prefix and "%s-%s"%(self.prefix, n) or "%s"%n), o), self.data.keys()))
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
                                        value = int(value)
                                        value = str(dict(f.fields[0].choices).get(value))
                                    except:
                                        raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
                                else:
                                    value = value
                            if year:
                                pass # FIXME: Append year to value?
                            attributes[key] = value 
            elif isinstance(f, forms.FileField):
                value = self.get_display_value_file_field(n)
                if value:
                    attributes[key] = value
            elif isinstance(f, forms.DecimalField):
                value = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                if value:
                    value = str(value)
                    attributes[key] = value
            else:
                value = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                if value:
                    attributes[key] = value
            #if i == len(self.fields.items())-1:
            #    if activity["main_tag"]["value"] and (attributes or activity["comment"]):
            #        attributes.append(deepcopy(activity))
        return attributes

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
        for (field_name, field) in cls().fields.items():
            prefixed_name = prefix and "%s-%s"%(prefix, field_name) or field_name
            if field_name.startswith('tg_'):
                taggroup = cls.get_data_for_tg_field(data, field_name, deal, prefixed_name, taggroup)

            else:
                tags, taggroup = cls.get_tags(field_name, deal, taggroup)

                if tags and len(tags) > 0:
                    if isinstance(field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)):
                        data.setlist(prefixed_name, cls.get_multiple_choice_data(field, field_name, taggroup))
                    else:
                        # Year based data?
                        if isinstance(field, forms.MultiValueField):
                            cls.get_year_based_data(data, field, field_name, prefixed_name, tags, taggroup)
                        else:
                            cls.get_other_data(data, field, field_name, prefixed_name, taggroup, tags)
        return data

    @classmethod
    def get_other_data(cls, data, field, field_name, prefixed_name, taggroup, tags):
        # if cls.DEBUG: print('get_other_data')
        if isinstance(taggroup, ActivityAttributeGroup) and taggroup.attributes.get(field_name):
            value = taggroup.attributes[field_name]
        elif hasattr(taggroup, field_name):
            value = getattr(taggroup, field_name)
        elif field_name in tags:
            value = tags[field_name]
        else:
            # if cls.DEBUG: print('didnt find %s' % field_name)
            value = None
        date = tags['date'] if 'date' in tags else None # tags.date or taggroup.date
        # if cls.DEBUG: print('        value, date', value, date)

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
    def get_multiple_choice_data(cls,  field, field_name, taggroup):
        tag_values = set([group.attributes[field_name] for group in taggroup if field_name in group.attributes])
        if cls.DEBUG: print('get_multiple_choice_data()', field_name, list(field.choices), tag_values)
        values = []
        for tag_value in tag_values:
            value = cls.get_multiple_choice_value(field, tag_value)
            if value:
                values.append(value)
        if cls.DEBUG: print('data[...] =', values, type(values).__name__)
        return values

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
        # if cls.DEBUG: print('get_year_based_data()', field_name, tags.get(field_name))
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
            tags = {str(field_name): taggroup.attributes.get(str(field_name))}
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

    def get_fields_display(self):
        """Return fields for detail view"""
        output = []
        tg_title = ''
        tg_items = []
        for i, (field_name, field) in enumerate(self.fields.items()):

            if field_name.startswith("tg_"):
                if field_name.endswith("_comment"):
                    data = self.initial.get(self.prefix and "%s-%s"%(self.prefix, field_name) or field_name, [])
                    if data:
                        tg_items.append((field.label, data))
                    continue
                if len(tg_items) > 0:
                    output.append(('tg', tg_title))
                    output.extend(tg_items)
                tg_title = field.initial
                tg_items = []
                continue

            if isinstance(field, NestedMultipleChoiceField):
                value = self.get_display_value_nested_multiple_choice_field(field, field_name)
            elif isinstance(field, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)):
                value = self.get_display_value_multiple_choice_field(field, field_name)
            elif isinstance(field, forms.ModelChoiceField):
                value = self.get_display_value_model_choice_field(field_name) # FIXME: Rename method
            elif isinstance(field, forms.ChoiceField):
                value = self.get_display_value_choice_field(field, field_name)
            elif isinstance(field, forms.MultiValueField):
                value = self.get_display_value_multi_value_field(field, field_name)
            elif isinstance(field, forms.FileField):
                value = self.get_display_value_file_field(field_name)
            else:
                value = self.is_valid() and self.cleaned_data.get(field_name) or self.initial.get(self.prefix and "%s-%s"%(self.prefix, field_name) or field_name)

            if value:
                tg_items.append({
                    'name': field_name,
                    'label': field.label,
                    'value': '%s %s' % (value, field.help_text),
                })

        if len(tg_items) > 0:
            output.append({
                'name': 'tg',
                'label': '',
                'value': tg_title,
            })
            output.extend(tg_items)

        return output

    def get_display_value_file_field(self, field_name):
        value = self.is_valid() and self.cleaned_data.get(field_name) and hasattr(self.cleaned_data.get(field_name),
            "name") and self.cleaned_data.get(field_name).name or self.data.get(self.prefix and "%s-%s" % (
                self.prefix, field_name) or field_name)
        return value

    def get_display_value_multi_value_field(self, field, field_name):
        # todo - fails with historical deals?
        data = self.initial.get(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, '')
        data = ensure_is_year_based_data(data)
        value, year = data.split(':')
        if value:
            if isinstance(field.fields[0], forms.ChoiceField):
                value = ', '.join([str(l) for v, l in field.fields[0].choices if str(v) == str(value)])
            if year:
                value += ' ({})'.format(year[:4])
        return value

    def get_display_value_choice_field(self, field, field_name):
        data = self.get_list_from_initial(field_name)
        value = '<br>'.join([str(l) for v, l in field.choices if str(v) in data])
        return value

    def get_list_from_initial(self, field_name):
        if isinstance(self.initial, MultiValueDict):
            return self.initial.getlist(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        data = self.initial.get(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        if data: data = [data]
        return data

    def get_display_value_multiple_choice_field(self, field, field_name):
        data = self.initial.get(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        value = '<br>'.join([str(l) for v, l in field.choices if str(v) in data])
        return value

    def get_display_value_nested_multiple_choice_field(self, field, field_name):
        data = self.initial.get(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        values = []
        for v, l, c in field.choices:
            value = ''
            if str(v) in data:
                value = str(l)
            if c:
                choices = ', '.join([str(l) for v, l in c if str(v) in data])
                value = (value and '%s (%s)' % (value, choices)) or choices
            if value:
                values.append(value)
        value = '<br>'.join(values)
        return value

    def get_display_value_model_choice_field(self, field_name):
        value = self.initial.get(self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        return str(value)

    class Meta:
        exclude = ()
        fields = ()
        readonly_fields = ()
        name = ''

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        #self.helper = FormHelper()
        #self.helper.form_method = 'post'
        #self.helper.form_tag = False
        #self.helper.form_class = 'form-horizontal'
        #self.helper.label_class = 'col-sm-2'
        #self.helper.field_class = 'col-sm-8'

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


def ensure_is_year_based_data(data):
    data = data.replace('::', ':')
    if ':' not in data:
        data += ':'
    return data
