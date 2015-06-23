__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import BrowseCondition

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


class BrowseConditionForm(BaseModelForm):
    variable = forms.ChoiceField(required=False, label=_("Variable"), initial="", choices=())
    operator = forms.ChoiceField(required=False, label=_("Operator"), initial="", choices=(), widget=forms.Select(attrs={"class": "operator"}))
    value = forms.CharField(required=False, label=_("Value"), initial="", widget=BrowseTextInput())

    def __init__(self, variables_activity=None, variables_investor=None, *args, **kwargs):
        super(BrowseConditionForm, self).__init__(*args, **kwargs)
        variables = []
        variables.append(("", "-----"))
        variables.append(("-1", "ID"))
        variables.append(("-2", "Deal scope"))
        variables.append(("fully_updated", "Fully updated"))
        variables.append(("fully_updated_by", "Fully updated by"))
        variables.append(("last_modification", "Last modification"))
        variables.append(("inv_-2", "Primary investor"))
        # TODO: fix these! This form was very tied to the old key value storage system
        # if variables_activity:
        #     self.a_fields = [(unicode(key.id), get_field_by_a_key_id(key.id)) for key in A_Key.objects.filter(fk_language=1, key__in=variables_activity)]#FIXME language
        # else:
        #     self.a_fields = [(unicode(key.id), get_field_by_a_key_id(key.id)) for key in A_Key.objects.filter(fk_language=1)]#FIXME language
        # if variables_investor:
        #     self.sh_fields = [("inv_%s" % key.id, get_field_by_sh_key_id(key.id)) for key in SH_Key.objects.filter(fk_language=1, key__in=variables_investor).exclude(key="name")]#FIXME language
        # else:
        #     self.sh_fields = [("inv_%s" % key.id, get_field_by_sh_key_id(key.id)) for key in SH_Key.objects.filter(fk_language=1).exclude(key="name")]#FIXME language
        # variables.extend([(f[0], unicode(f[1].label)) for f in self.a_fields])
        # variables.extend([(f[0], "Investor %s" % unicode(f[1].label)) for f in self.sh_fields])
        variables = sorted(variables, key=lambda x: x[1])
        self.fields["variable"].choices = variables
        operators = []
        operators.append(("", "-----"))
        operators.extend([(op, op_name[2]) for op, op_name in ActivityProtocol.OPERATION_MAP.items()])
        self.fields["operator"].choices = operators


    #def save(self, *args, **kwargs):
        #raise IOError, self.cleaned_data["value"]
        #c = super(BrowseConditionForm, self).save(commit=False)
        #if c.variable:
        #    try:
        #        f = dict(self.a_fields)[c.variable]
        #    except:
        #        try:
        #            f = dict(self.sh_fields)[c.variable]
        #        except:
        #            f = None
        #    # single value field?
        #    if f and not isinstance(f.widget, forms.SelectMultiple) and not c.operator in ("in", "not_in"):
        #        c.value = c.value[3:-2]
        #    # multiple value field saved by admin (e.g. [u'[1,2,3]'])?
        #    elif c.value.startswith("[u'["):
        #        c.value = c.value[3:-2]
        #    c.save()
    #    return c

    class Meta:
        model = BrowseCondition
        exclude = ('rule',)
