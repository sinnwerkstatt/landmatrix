import datetime
from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.translation import ugettext_lazy as _

from grid.views.browse_filter_conditions import get_field_by_key
from grid.fields import YearMonthDateField


class FilterWidgetAjaxView(APIView):

    renderer_classes = (JSONRenderer,)

    TYPE_STRING = 'string'
    TYPE_NUMERIC = 'numeric'
    TYPE_BOOLEAN = 'boolean'
    TYPE_LIST = 'list'
    TYPE_AUTOCOMPLETE = 'autocomplete'
    TYPE_LIST_MULTIPLE = 'multiple'
    TYPE_DATE = 'date'
    FIELD_TYPE_MAPPING = OrderedDict((
        (YearMonthDateField, TYPE_DATE), # Placed before CharField since it inherits from CharField
        (forms.CharField, TYPE_STRING),
        (forms.IntegerField, TYPE_NUMERIC),
        (forms.BooleanField, TYPE_BOOLEAN),
        (forms.ChoiceField, TYPE_LIST),
        (forms.MultipleChoiceField, TYPE_LIST_MULTIPLE),
    ))
    FIELD_NAME_TYPE_MAPPING = {
        'activity_identifier': TYPE_NUMERIC,
        'fully_updated': TYPE_DATE,
        'fully_updated_date': TYPE_DATE,
        'last_modification': TYPE_DATE,
        'fully_updated_by': TYPE_LIST,
        'operational_stakeholder': TYPE_AUTOCOMPLETE,
        'target_country': TYPE_AUTOCOMPLETE,
    }
    TYPE_OPERATION_MAPPING = {
        TYPE_STRING: ('contains', 'is', 'is_empty'),
        TYPE_NUMERIC: ('lt', 'gt', 'gte', 'lte', 'is', 'is_empty'),
        TYPE_BOOLEAN: ('is', 'is_empty'),
        TYPE_LIST: ('is', 'not_in', 'in', 'is_empty'),
        TYPE_LIST_MULTIPLE: ('is', 'not_in', 'in', 'is_empty'),
        TYPE_DATE: ('lt', 'gt', 'gte', 'lte', 'is', 'is_empty'),
        TYPE_AUTOCOMPLETE: ('is', 'not_in', 'in', 'is_empty'),
    }
    OPERATION_WIDGET_MAPPING = {
        'is_empty': None,
    }
    TYPE_WIDGET_MAPPING = {
        TYPE_STRING: [
            {
                'operations': ('contains', 'is'),
                'widget': forms.TextInput,
            }
        ],
        TYPE_NUMERIC: [
            {
                'operations': ('lt', 'gt', 'gte', 'lte', 'is'),
                'widget': forms.NumberInput,
            }
        ],
        TYPE_BOOLEAN: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            }
        ],
        TYPE_LIST: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.CheckboxSelectMultiple,
            }
        ],
        TYPE_LIST_MULTIPLE: [
            {
                'operations': ('is',),
                'widget': forms.CheckboxSelectMultiple,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.CheckboxSelectMultiple,
            }
        ],
        TYPE_DATE: [
            {
                'operations': ('lt', 'gt', 'gte', 'lte', 'is'),
                'widget': DateTimePicker,
            }
        ],
        TYPE_AUTOCOMPLETE: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.SelectMultiple,
            }
        ],
    }
    FIELD_NAME_MAPPING = {
        'operational_stakeholder': 'operating_company_id',
    }
    field_name = ''
    name = ''
    operation = ''

    def get(self, *args, **kwargs):
        """ render form to enter values for the requested field in the filter widget for the grid view
            form to select operations is updated by the javascript function update_widget() in /media/js/main.js
        """
        self.field_name = self.request.GET.get('key_id', '')
        self.name = self.request.GET.get('name', '')
        self.operation = self.request.GET.get('operation', '')

        return Response({
            'allowed_operations': self.get_allowed_operations(),
            'widget': self.render_widget()
        })

    @property
    def field(self):
        if not hasattr(self, '_field'):
            if self.field_name:
                # Deprecated?
                if "inv_" in self.field_name:
                    field = get_field_by_key(self.field_name[4:])
                else:
                    field = get_field_by_key(self.field_name)
                # MultiValueField?
                if isinstance(field, forms.MultiValueField):
                    # Get first field instead
                    field = field.fields[0]
                self._field = field
        return self._field

    @property
    def type(self):
        field = self.field
        if not hasattr(self, '_type'):
            # Get type by field class
            for field_class, field_type in self.FIELD_TYPE_MAPPING.items():
                if isinstance(field, field_class):
                    self._type = field_type
                    break
            # Get type by field name
            if self.field_name in self.FIELD_NAME_TYPE_MAPPING.keys():
                self._type = self.FIELD_NAME_TYPE_MAPPING.get(self.field_name)
            # Fallback to string
            if not hasattr(self, '_type'):
                self._type = self.TYPE_STRING
        return self._type

    @property
    def value(self):
        if not hasattr(self, '_value'):
            value = self.request.GET.get('value', '')
            if value:
                # Date?
                if self.type == self.TYPE_DATE:
                    value = datetime.strptime(value, "%Y-%m-%d")
            else:
                # Boolean?
                if self.type == self.TYPE_BOOLEAN:
                    value = 'True'
            # Make list
            if self.type in (self.TYPE_LIST, self.TYPE_LIST_MULTIPLE):
                self._value = value and value.split(',') or []
            else:
                self._value = value
        return self._value

    def get_allowed_operations(self):
        return self.TYPE_OPERATION_MAPPING[self.type]

    def get_attrs(self):
        # Merge custom with existing field attributes
        attrs = {
            'id': 'id_{}'.format(self.name),
        }
        if not self.field or not hasattr(self.field.widget, 'attrs'):
            return attrs
        if not self.type == self.TYPE_LIST_MULTIPLE and \
           not (self.type == self.TYPE_LIST and self.operation in ('in', 'not_in')):
            attrs['class'] = 'valuefield form-control'
        field_attrs = self.field.widget.attrs
        for key, value in field_attrs.items():
            if key in ('readonly',):
                continue
            if key in attrs and key == 'class':
                attrs[key] += ' %s' % field_attrs[key]
            else:
                attrs[key] = field_attrs[key]
        return attrs

    def get_widget_init_kwargs(self):
        kwargs = {}
        # Get boolean choices (Yes/No)
        if self.type == self.TYPE_BOOLEAN:
            kwargs['choices'] = [
                ('True', _('Yes')),
                ('False', _('No')),
            ]
        # Get list choices
        if self.type in (self.TYPE_LIST, self.TYPE_LIST_MULTIPLE):
            if self.field_name == 'fully_updated_by':
                users = User.objects.filter(groups__name__in=("Research admins",
                                            "Research assistants")).order_by("username")
                kwargs['choices'] = [(u.id, u.get_full_name() or u.username) for u in users]
            else:
                kwargs['choices'] = self.field.choices
        # Get date options
        if self.type == self.TYPE_DATE:
            kwargs['options'] = {
                "format": "YYYY-MM-DD",
                "inline": True,
            }
        return kwargs

    def get_widget_render_kwargs(self):
        return {
            'name': self.name,
            'value': self.value,
            'attrs': self.get_attrs()
        }

    def get_widget_class(self):
        operation_mappings = self.TYPE_WIDGET_MAPPING[self.type]
        widget = None
        for operation_mapping in operation_mappings:
            if self.operation in operation_mapping['operations']:
                widget = operation_mapping['widget']
        return widget

    def render_widget(self):
        widget = self.get_widget_class()
        if widget:
            widget = widget(**self.get_widget_init_kwargs())
            widget = self._pre_render_widget(widget)
            widget = widget.render(**self.get_widget_render_kwargs())
            widget = self._post_render_widget(widget)
        return widget

    def _pre_render_widget(self, widget):
        if self.type == self.TYPE_DATE:
            # See here: https://github.com/jorgenpt/django-bootstrap3-datetimepicker/commit/042dd1da3a7ff21010c1273c092cba108d95baeb#commitcomment-16877308
            widget.js_template = """
            <script>
                    $(function(){$("#%(picker_id)s:has(input:not([readonly],[disabled]))")
                    .datetimepicker(%(options)s);});
            </script>
            """
        return widget

    def _post_render_widget(self, widget):
        return widget
