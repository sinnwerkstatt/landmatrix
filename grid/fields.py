from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.contrib.gis.forms import MultiPolygonField
from django.conf import settings
from django.core import validators


from landmatrix.models import Country
from grid.widgets import (
    YearBasedSelect, YearBasedTextInput, YearBasedSelectMultiple,
    YearBasedSelectMultipleNumber, YearBasedCheckboxInput,
    NestedCheckboxSelectMultiple, TitleWidget, PrimaryInvestorSelect,
    FileInputWithInitial, MultiTextInput, CountrySelect, TextChoiceInput,
    AreaWidget,
)


class YearMonthDateValidator(validators.RegexValidator):
    # Allow YYYY or YYYY-MM or YYYY-MM-DD
    regex = '^([0-9]{4}|[0-9]{4}-[0-9]{2}|[0-9]{4}-[0-9]{2}-[0-9]{2})$'

class YearMonthDateField(forms.CharField):
    default_validators = [
        YearMonthDateValidator()
    ]

class YearBasedField(forms.MultiValueField):
    '''
    Base class for year based fields, since there are some isinstance
    checks to handle them.
    TODO: remove those, use duck typing.
    TODO: probably, some logic is shared among the year based fields.
    move that here.
    '''
    pass


class YearBasedBooleanField(YearBasedField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.BooleanField(required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedCheckboxInput(help_text=kwargs.pop("help_text", ""))
        super(YearBasedBooleanField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/3):
                self.fields.extend([
                    forms.BooleanField(required=False),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedBooleanField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)/3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.IntegerField(required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False)
            ]


class YearBasedIntegerField(YearBasedField):

    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.IntegerField(required=False),
            YearMonthDateField(required=False),
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
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedIntegerField, self).clean(value)

    def compress(self, data_list):
        """  """
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]


class YearBasedFloatField(YearBasedField):

    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.FloatField(required=False, localize=True),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False)
        ]
        if 'placeholder' in kwargs:
            attrs = {'placeholder': kwargs.pop('placeholder', None)}
        else:
            attrs = {}
        kwargs["widget"] = YearBasedTextInput(help_text=kwargs.pop("help_text", ""), attrs=attrs)
        super(YearBasedFloatField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.FloatField(required=False, localize=True),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedFloatField, self).clean(value)

    def compress(self, data_list):
        """  """
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [forms.FloatField(required=False, localize=True), YearMonthDateField(required=False)]


class YearBasedChoiceField(YearBasedField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.ChoiceField(choices=kwargs["choices"], required=False), YearMonthDateField(required=False)]
        kwargs["widget"] = YearBasedSelect(choices=kwargs.pop("choices"), help_text=kwargs.pop("help_text", ""),attrs={})
        super(YearBasedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.ChoiceField(choices=self.choices, required=False),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ChoiceField(choices=self.choices, required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False)
            ]


class YearBasedModelMultipleChoiceField(YearBasedField):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        kwargs["fields"] = [forms.ModelMultipleChoiceField(queryset=self.queryset, required=False), YearMonthDateField(required=False)]
        kwargs["widget"] = YearBasedSelectMultiple(choices=kwargs['fields'][0].choices, help_text=kwargs.pop("help_text", ""),attrs={})
        super(YearBasedModelMultipleChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedModelMultipleChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False)
            ]


class YearBasedModelMultipleChoiceIntegerField(YearBasedField):
    placeholder = _('Size')
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        if 'placeholder' in kwargs:
            attrs = {'placeholder': kwargs.pop("placeholder")}
        else:
            attrs = {}
        kwargs["fields"] = [
            forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
            forms.IntegerField(required=False),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False),
        ]
        kwargs["widget"] = YearBasedSelectMultipleNumber(
            choices=kwargs['fields'][0].choices,
            help_text=kwargs.pop("help_text", ""),
            attrs=attrs
        )
        super(YearBasedModelMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//4):
                self.fields.extend([
                    forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                    forms.IntegerField(required=False),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False),
                ])
        return super(YearBasedModelMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//4):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                forms.IntegerField(required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False),
            ]


class YearBasedMultipleChoiceIntegerField(YearBasedField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        kwargs["fields"] = [
            forms.MultipleChoiceField(choices=self.choices, required=False),
            forms.IntegerField(required=False),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False),
        ]
        kwargs["widget"] = YearBasedSelectMultipleNumber(
            choices=self.choices,
            help_text=kwargs.pop("help_text", ""),
            attrs={}
        )
        super(YearBasedMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//4):
                self.fields.extend([
                    forms.MultipleChoiceField(choices=self.choices, required=False),
                    forms.IntegerField(required=False),
                    YearMonthDateField(required=False),
                    forms.BooleanField(required=False),
                ])
        return super(YearBasedMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//4):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or ''),
                        str(data_list[i+2] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.MultipleChoiceField(choices=self.choices, required=False),
                forms.IntegerField(required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False),
            ]


class MultiCharField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.CharField(required=False)]
        kwargs["widget"] = MultiTextInput(help_text=kwargs.pop("help_text", ""), attrs={})
        super(MultiCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)):
                self.fields.append(forms.CharField(required=False))
        return super(MultiCharField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            data = []
            for i in range(len(data_list)):
                if data_list[i]:
                    data.append(str(data_list[i]))
            return "#".join(data)
        else:
            self.fields = [forms.CharField(required=False)]


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % obj.get_full_name() or obj.username


class TitleField(forms.CharField):
    '''
    TODO: default to required=False and label="" (repeated everywhere)
    '''
    widget = TitleWidget
    is_title = True

    def __init__(self, *args, **kwargs):
        self.widget = TitleWidget(initial=kwargs.get("initial"))
        super().__init__(*args, **kwargs)


class PrimaryInvestorField(forms.ChoiceField):
    widget = PrimaryInvestorSelect
    # TODO: fix
    queryset = lambda x: []

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.get_choices()
        super(PrimaryInvestorField, self).__init__(*args, **kwargs)

    def get_choices(self):
        return self.queryset()


class NestedMultipleChoiceField(forms.MultipleChoiceField):

    widget = NestedCheckboxSelectMultiple

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        return value in self._valid_keys()

    def _valid_keys(self):
        values = []
        for k, v, sub_choices in self.choices:
            values.append(k)
            if isinstance(sub_choices, (list, tuple)):
                for k2, v2 in sub_choices:
                    values.append(k2)
        return values

    def get_value(self, key):
        for k, v, c in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if key == smart_text(k2):
                        return v2
            else:
                if key == smart_text(k):
                    return v
                elif c:
                    for k2, v2 in c:
                        if k == smart_text(k2):
                            return v2


class FileFieldWithInitial(forms.FileField):
    widget = FileInputWithInitial
    show_hidden_initial = True

    def validate(self, value):
        '''
        For new uploads only, check that size is less than our max.

        This doesn't prevent DOS attacks (for that we'd need to limit the
        webserver) but it does let us give the user a nice error message.
        '''
        if value and value._size > settings.DATA_SOURCE_MAX_UPLOAD_SIZE:
            raise ValidationError(_("Uploaded files must be less than 10MB."))


class CountryField(forms.ModelChoiceField):

    widget = CountrySelect(attrs={"readonly":"readonly"})

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Country.objects.defer('geom').all().order_by("name")
        super(CountryField, self).__init__(*args, **kwargs)


class ActorsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.CharField(required=False), forms.ChoiceField(choices=kwargs["choices"], required=False)]
        kwargs["widget"] = TextChoiceInput(choices=kwargs.pop("choices"), help_text=kwargs.pop("help_text", ""), attrs={})
        super(ActorsField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//2):
                self.fields.extend([forms.CharField(required=False), forms.ChoiceField(choices=self.choices, required=False)])
        return super(ActorsField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (
                        str(data_list[i] or ''),
                        str(data_list[i+1] or '')
                    ))
            return "#".join(yb_data)
        else:
            self.fields = [forms.CharField(required=False), forms.ChoiceField(choices=self.choices, required=False)]


class MultiFileField(forms.FileField):
    '''
    Prevent upload error for multiple files
    '''
    def to_python(self, data):
        for file in data:
            if file in self.empty_values:
                return None

            # UploadedFile objects should have name and size attributes.
            try:
                file_name = file.name
                file_size = file.size
            except AttributeError:
                raise ValidationError(self.error_messages['invalid'], code='invalid')

            if self.max_length is not None and len(file_name) > self.max_length:
                params = {'max': self.max_length, 'length': len(file_name)}
                raise ValidationError(self.error_messages['max_length'], code='max_length', params=params)
            if not file_name:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
            if not self.allow_empty_file and not file_size:
                raise ValidationError(self.error_messages['empty'], code='empty')
        return data


class AreaField(forms.MultiValueField):
    '''
    MultiValueField for area map with optional shapefile upload.

    Note because of Django's handling of multiple files, compress here
    doesn't do anything with shapefiles, it just returns one (of the several
    required) if there was one.
    '''

    def __init__(self, *args, **kwargs):
        fields = (
            MultiPolygonField(required=False),
            forms.FileField(required=False)
        )
        kwargs.update({
            'fields': fields,
            'require_all_fields': False,
            'widget': AreaWidget,
        })
        super().__init__(*args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Second value (file field) takes precedence
            value = data_list[1] or data_list[0]
        else:
            value = None

        return value

