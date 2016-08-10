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
from grid.widgets.nested_multiple_choice_field import NestedMultipleChoiceField

class BaseForm(forms.Form):
    DEBUG = False
    error_css_class = "error"

    def get_attributes(self, request=None):
        """
        Get posted form data, for saving to the database.
        For activity or stakeholder, using attribute group only - if given
        (for formsets)
        """
        attributes = {}
        for i, (n, f) in enumerate(self.fields.items()):
            name = str(n)
            # New tag group?
            if n.startswith('tg_') and not n.endswith('_comment'):
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
                values = []
                for v in list(value):
                    if v:
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
                            values.append({'value': value})
                if values:
                    attributes[name] = values
            elif isinstance(f, forms.ChoiceField):
                #tag["op"] = "select"
                value = self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
#                if activity["main_tag"]["value"] == "investor":
#                    raise IOError, self.data
#                if activity["main_tag"]["value"] == "investor" and value:
#                    raise IOError, n
                # quickfix for receiving 'Non' as a value FIXME
                if value and value != "0" and value != "Non":
                    if name in ("investor", "primary_investor"):
                        attributes[name] = value
                    else:
                        try:
                            if hasattr(f, 'queryset'):
                                value = int(value)
                            value = str(dict(f.choices).get(value))
                            if value:  
                                attributes[name] = {'value': value}
                        except:
                            raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
            # Year based data?
            elif isinstance(f, forms.MultiValueField):
                keys = list(filter(lambda o: re.match(r'%s_\d+'% (self.prefix and "%s-%s"%(self.prefix, n) or "%s"%n), o), self.data.keys()))
                keys.sort()
                values = []
                for i in range(len(keys)):
                    count = len(f.widget.get_widgets())
                    if i % count == 0:
                        value = self.data.get(len(keys) > i and keys[i] or "-", "")
                        value2 = None
                        if count > 2:
                            value2 = self.data.get(len(keys) > i+1 and keys[i+1] or "-", "")
                            value2 = self.data.get(len(keys) > i+2 and keys[i+2] or "-", "")
                        else:
                            year = self.data.get(len(keys) > i+1 and keys[i+1] or "-", "")
                        if value or value2 or year:
                            #if value and isinstance(f.fields[0], forms.ChoiceField):
                            #    try:
                            #        value = str(dict(f.fields[0].choices).get(value))
                            #    except:
                            #        raise IOError("Value '%s' for field %s (%s) not allowed." % (value, n, type(self)))
                            #if value2 and isinstance(f.fields[0], forms.ChoiceField):
                            #    try:
                            #        value2 = str(dict(f.fields[0].choices).get(value2))
                            #    except:
                            #        raise IOError("Value '%s' for field %s (%s) not allowed." % (value2, n, type(self)))
                            values.append({
                                'value': value,
                                'value2': value2,
                                'date': year,
                            })

                if name == 'contract_size':
                    data = self.data
                    raise IOError(values)
                if values:
                    attributes[name] = values
            elif isinstance(f, forms.FileField):
                value = self.get_display_value_file_field(n)
                if value:
                    attributes[name] = {'value': value}
            elif isinstance(f, forms.DecimalField):
                value = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                if value:
                    attributes[name] = {'value': str(value)}
            else:
                value = self.is_valid() and self.cleaned_data.get(n) or self.data.get(self.prefix and "%s-%s"%(self.prefix, n) or n)
                if value:
                    attributes[name] = {'value': value}
            #if i == len(self.fields.items())-1:
            #    if activity["main_tag"]["value"] and (attributes or activity["comment"]):
            #        attributes.append(deepcopy(activity))
        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        """
        Load previously saved attributes from the database.
        Returns:
        {
            'Name of attribute 1': {
                value: 'Value for attribute',
                value2: 'Optional second value for attribute, e.g. ha for crops',
                date: 'Date of value for year based fields',
            },
            'Name of attribute 2': {
                ...
            }
        }
        """
        data = MultiValueDict()

        # Create attributes dict
        queryset = activity.attributes
        if group:
            queryset = queryset.filter(fk_group__name=group)
        attributes = dict()
        for aa in queryset.all():
            if aa.name in attributes:
                attributes[aa.name].append(aa)
            else:
                attributes[aa.name] = [aa]

        for (field_name, field) in cls().base_fields.items():
            # Group title?
            name = prefix and "%s-%s"%(prefix, field_name) or field_name
            if field_name.startswith('tg_') and not field_name.endswith('comment'):
                continue
            #tags, group = cls.get_tags(field_name, activity, group)
            attribute = attributes.get(field_name, [])

            if not attribute:
                continue

            value = attribute[0].value
            # Multiple choice?
            if isinstance(field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)):
                value = cls.get_multiple_choice_data(field, field_name, attribute)
            # Year based data?
            elif isinstance(field, forms.MultiValueField):
                value = cls.get_year_based_data(field, field_name, attribute)
            # Choice field?
            elif isinstance(field, forms.ChoiceField):
                for k, v in field.choices:
                    if v == value:
                        value = str(k)
                        break
            # Date field?
            elif isinstance(field, forms.DateField):
                # reformat date values
                try:
                    value = datetime.strptime(value, "%Y-%m-%d").strftime("%d:%m:%Y")
                except:
                    # catch invalid date formats from import
                    pass
                
            if value:
                data[name] = value
        return data

    @classmethod
    def get_multiple_choice_data(cls,  field, field_name, attributes):
        values = []
        for attribute in attributes:
            value = cls.get_multiple_choice_value(field, attribute.value)
            if value:
                values.append(value)
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
                if k == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                    return str(k)
        return None

    @classmethod
    def get_choice_value(cls, field, tag_value):
        for k, v in [i[:2] for i in field.choices]:
            if k == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                return str(k)
        return None

    @classmethod
    def get_year_based_data(cls, field, field_name, attributes):
        # Group all attributes by date
        attributes_by_date = dict()
        # Some year based fields take 2 values, e.g. crops and area
        values_count = len(field.widget.get_widgets()) - 1
        values = []
        for attribute in attributes:
            #if isinstance(field.fields[0], forms.ChoiceField):
            #    for k, v in field.fields[0].choices:
            #        if v == value:
            #            value = str(k)
            #            break
            if attribute.date in attributes_by_date:
                if attribute.value:
                    attributes_by_date[attribute.date][0] += ',' + attribute.value
                if values_count > 1 and attribute.value2:
                    attributes_by_date[attribute.date][1] += ',' + attribute.value2
            else:
                if values_count == 1:
                    attributes_by_date[attribute.date] = [attribute.value]
                else:
                    attributes_by_date[attribute.date] = [attribute.value, attribute.value2 or '']  
        if values_count == 1:
            values = [':'.join([a[0], d or '']) for d, a in attributes_by_date.items()]
        else:
            values = [':'.join([a[0], a[1], d or '']) for d, a in attributes_by_date.items()]
        return '#'.join(values)

#    @classmethod
#    def get_tags(cls, field_name, deal, group):
#        if not deal and not group:
#            return [], None
#
#        if isinstance(deal, Deal):
#            tags = deal.attributes
#            if not group:
#                group = list(deal.attribute_groups())
#        # elif isinstance(group, SH_Tag_Group):
#        #     tags = group.sh_tag_set.filter(fk_sh_key__key=str(field_name))
#        elif group is None:
#            return None, None
#        else:
#            tags = {str(field_name): group.attributes.get(str(field_name))}
#        return tags, group

#    @classmethod
#    def get_data_for_tg_field(cls, data, field_name, deal, pn, group):
#
#        if field_name.endswith('_comment'):
#
#            groups = group if isinstance(group, list) else [group]
#            comments = BaseForm.get_comments_from_groups(groups)
#            cls.fill_comment_field(comments, data, field_name, pn)
#
#        elif not group:
#            try:
#                if isinstance(deal, Stakeholder):
#                    group = deal.sh_tag_group_set.get(fk_sh_tag__fk_sh_value__value=field_name[3:])
#                else:
#                    group = deal.a_tag_group_set.get(fk_a_tag__fk_a_value__value=field_name[3:])
#            except:
#                group = None
#        return group

    @classmethod
    def fill_comment_field(cls, comments, data, field_name, pn):
        if comments and field_name[3:] in comments:
            data[pn] = comments[field_name[3:]]

    @classmethod
    def get_comments_from_groups(cls, groups):
        return dict([(k, v) for group in [g for g in groups if g] for (k, v) in group.attributes.items() if '_comment' in k])

    def get_fields_display(self):
        """Return fields for detail view"""
        output = []
        tg_title = ''
        tg_items = []
        for i, (field_name, field) in enumerate(self.base_fields.items()):

            if field_name.startswith("tg_") and not field_name.endswith("_comment"):
                #    value = self.initial.get(self.prefix and "%s-%s"%(self.prefix, field_name) or field_name, [])
                #    if field_name == 'tg_nature_comment':
                #        raise IOError(value)
                #    if value:
                #        tg_items.append(field.label, value))
                #    continue
                if len(tg_items) > 0:
                    output.append({
                        'name': 'tg',
                        'label': '',
                        'value': tg_title,
                    })
                    output.extend(tg_items)
                tg_title = field.initial
                tg_items = []
                continue
            if isinstance(field, NestedMultipleChoiceField):
                value = self.get_display_value_nested_multiple_choice_field(field, field_name)
            elif isinstance(field, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)):
                value = self.get_display_value_multiple_choice_field(field, field_name)
            elif isinstance(field, forms.ModelChoiceField):
                value = self.get_display_value_model_choice_field(field, field_name)
            elif isinstance(field, forms.ChoiceField):
                value = self.get_display_value_choice_field(field, field_name)
            elif isinstance(field, forms.MultiValueField):
                value = self.get_display_value_multi_value_field(field, field_name)
            elif isinstance(field, forms.FileField):
                value = self.get_display_value_file_field(field_name)
            elif isinstance(field, forms.BooleanField):
                value = self.get_display_value_boolean_field(field_name)
            else:
                value = self.initial.get(field_name, '')#self.prefix and "%s-%s"%(self.prefix, field_name) or field_name)

            if value:
                tg_items.append({
                    'name': field_name,
                    'label': field.label,
                    'value': value,
                    #'value': '%s %s' % (value, field.help_text),
                })

        if len(tg_items) > 0:
            output.append({
                'name': 'tg',
                'label': '',
                'value': tg_title,
            })
            output.extend(tg_items)
        return output

    def get_display_value_boolean_field(self, field_name):
        data = self.initial.get(field_name, '')#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, '')
        if data == 'True':
            return _('Yes')
        elif data == 'False':
            return _('No')
        return ''

    def get_display_value_file_field(self, field_name):
        value = self.initial.get(field_name, '')
        return value

    def get_display_value_multi_value_field(self, field, field_name):
        # todo - fails with historical deals?
        data = self.initial.get(field_name, '')#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, '')
        values = []
        if data:
            for value in data.split('#'):
                date_values = value.split(':')
                date = date_values.pop()
                if date_values:
                    if isinstance(field.fields[0], forms.ChoiceField):
                        selected = date_values[0].split(',')
                        date_values[0] = ', '.join([str(l) for v, l in field.fields[0].choices if str(v) in selected])
                    value = ''
                    if date:
                        value += '[%s] ' % date
                    value += ', '.join(filter(None, date_values))
                if value:
                    values.append(value)
        return '<br>'.join(values)

    def get_display_value_choice_field(self, field, field_name):
        data = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        value = '<br>'.join([str(l) for v, l in field.choices if v and str(v) in data])
        return value

#    def get_list_from_initial(self, field_name):
#        if isinstance(self.initial, MultiValueDict):
#            return self.initial.getlist(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
#        data = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
#        if data: data = [data]
#        return data

    def get_display_value_multiple_choice_field(self, field, field_name):
        data = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        value = '<br>'.join([str(l) for v, l in field.choices if str(v) in data])
        return value

    def get_display_value_nested_multiple_choice_field(self, field, field_name):
        data = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
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

    def get_display_value_model_choice_field(self, field, field_name):
        value = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        if value:
            return str(field.queryset.get(pk=value))
        else:
            return ''


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
                    if value and isinstance(f.choices,(list, tuple)) and f.choices[0][0] != 0:
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