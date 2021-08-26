from django.conf import settings
from django.contrib.gis.forms import MultiPolygonField
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from django.utils.translation import gettext_lazy as _

from apps.grid.widgets import *
from apps.ol3_widgets.widgets import OpenLayersWidget


class YearMonthDateValidator(validators.RegexValidator):
    # Allow YYYY or YYYY-MM or YYYY-MM-DD
    regex = "^([0-9]{4}|[0-9]{4}-[0-9]{2}|[0-9]{4}-[0-9]{2}-[0-9]{2})$"


class YearMonthDateField(forms.CharField):
    default_validators = [YearMonthDateValidator()]


class YearBasedField(forms.MultiValueField):
    """
    Base class for year based fields, since there are some isinstance
    checks to handle them.
    TODO: remove those, use duck typing.
    TODO: probably, some logic is shared among the year based fields.
    move that here.
    """

    pass


class YearBasedIntegerField(YearBasedField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.IntegerField(required=False),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False),
        ]
        if "placeholder" in kwargs:
            attrs = {"placeholder": kwargs.pop("placeholder", None)}
        else:
            attrs = {}
        kwargs["widget"] = YearBasedTextInput(
            help_text=kwargs.pop("help_text", ""), attrs=attrs
        )
        super(YearBasedIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 3):
                self.fields.extend(
                    [
                        forms.IntegerField(required=False),
                        YearMonthDateField(required=False),
                        forms.BooleanField(required=False),
                    ]
                )
        return super(YearBasedIntegerField, self).clean(value)

    def compress(self, data_list):
        """ """
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 3):
                j = i * 3
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s:%s"
                        % (
                            str(data_list[j] or ""),
                            str(data_list[j + 1] or ""),
                            str(data_list[j + 2] or ""),
                        )
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.IntegerField(required=False),
                forms.CharField(required=False),
            ]
            return ""


class YearBasedFloatField(YearBasedField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.FloatField(required=False, localize=True),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False),
        ]
        if "placeholder" in kwargs:
            attrs = {"placeholder": kwargs.pop("placeholder", None)}
        else:
            attrs = {}
        attrs["class"] = "year-based input-filter-number"
        kwargs["widget"] = YearBasedTextInput(
            help_text=kwargs.pop("help_text", ""), attrs=attrs
        )
        super(YearBasedFloatField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 3):
                self.fields.extend(
                    [
                        forms.FloatField(required=False, localize=True),
                        YearMonthDateField(required=False),
                        forms.BooleanField(required=False),
                    ]
                )
        return super(YearBasedFloatField, self).clean(value)

    def compress(self, data_list):
        """ """
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 3):
                j = i * 3
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s:%s"
                        % (
                            str(data_list[j] or ""),
                            str(data_list[j + 1] or ""),
                            str(data_list[j + 2] or ""),
                        )
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.FloatField(required=False, localize=True),
                YearMonthDateField(required=False),
            ]
            return ""


class YearBasedChoiceField(YearBasedField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [
            forms.ChoiceField(choices=kwargs["choices"], required=False),
            YearMonthDateField(required=False),
        ]
        kwargs["widget"] = YearBasedSelect(
            choices=kwargs.pop("choices"),
            help_text=kwargs.pop("help_text", ""),
            attrs={},
        )
        super(YearBasedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 3):
                self.fields.extend(
                    [
                        forms.ChoiceField(choices=self.choices, required=False),
                        YearMonthDateField(required=False),
                        forms.BooleanField(required=False),
                    ]
                )
        return super(YearBasedChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 3):
                j = i * 3
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s:%s"
                        % (
                            str(data_list[j] or ""),
                            str(data_list[j + 1] or ""),
                            str(data_list[j + 2] or ""),
                        )
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ChoiceField(choices=self.choices, required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False),
            ]
            return ""


class YearBasedModelMultipleChoiceIntegerField(YearBasedField):

    placeholder = _("ha")

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        if "placeholder" in kwargs:
            self.placeholder = kwargs.pop("placeholder")
        if self.placeholder:
            attrs = {"placeholder": self.placeholder}
        else:
            attrs = {}
        kwargs["fields"] = [
            forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
            forms.IntegerField(required=False),
            YearMonthDateField(required=False),
            forms.BooleanField(required=False),
        ]
        kwargs["widget"] = YearBasedSelectMultipleNumber(
            choices=kwargs["fields"][0].choices,
            help_text=kwargs.pop("help_text", ""),
            attrs=attrs,
        )
        super(YearBasedModelMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 4):
                self.fields.extend(
                    [
                        forms.ModelMultipleChoiceField(
                            queryset=self.queryset, required=False
                        ),
                        forms.IntegerField(required=False),
                        YearMonthDateField(required=False),
                        forms.BooleanField(required=False),
                    ]
                )
        return super(YearBasedModelMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 4):
                j = i * 4
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s:%s:%s"
                        % (
                            str(data_list[j] or ""),
                            str(data_list[j + 1] or ""),
                            str(data_list[j + 2] or ""),
                            str(data_list[j + 3] or ""),
                        )
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                forms.IntegerField(required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False),
            ]
            return ""


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
            choices=self.choices, help_text=kwargs.pop("help_text", ""), attrs={}
        )
        super(YearBasedMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 4):
                self.fields.extend(
                    [
                        forms.MultipleChoiceField(choices=self.choices, required=False),
                        forms.IntegerField(required=False),
                        YearMonthDateField(required=False),
                        forms.BooleanField(required=False),
                    ]
                )
        return super(YearBasedMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 4):
                j = i * 4
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s:%s:%s"
                        % (
                            str(data_list[j] or ""),
                            str(data_list[j + 1] or ""),
                            str(data_list[j + 2] or ""),
                            str(data_list[j + 3] or ""),
                        )
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.MultipleChoiceField(choices=self.choices, required=False),
                forms.IntegerField(required=False),
                YearMonthDateField(required=False),
                forms.BooleanField(required=False),
            ]
            return ""


class MultiCharField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.CharField(required=False)]
        kwargs["widget"] = MultiTextInput(
            help_text=kwargs.pop("help_text", ""), attrs={}
        )
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
            return ""


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """

    def label_from_instance(self, obj):
        return "%s" % obj.get_full_name() or obj.username


class TitleField(forms.CharField):
    """
    TODO: default to required=False and label="" (repeated everywhere)
    """

    widget = TitleWidget
    is_title = True

    def __init__(self, *args, **kwargs):
        self.widget = TitleWidget(initial=kwargs.get("initial"))
        super().__init__(*args, **kwargs)


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
            if key == smart_text(k):
                return v
            elif c:
                for k2, v2 in c:
                    if key == smart_text(k2):
                        return v2


class FileFieldWithInitial(forms.FileField):
    widget = FileInputWithInitial
    show_hidden_initial = True

    def validate(self, value):
        """
        For new uploads only, check that size is less than our max.

        This doesn't prevent DOS attacks (for that we'd need to limit the
        webserver) but it does let us give the user a nice error message.
        """
        if value and value.size > settings.DATA_SOURCE_MAX_UPLOAD_SIZE:
            raise ValidationError(_("Uploaded files must be less than 10MB."))


class CountryField(forms.ModelChoiceField):

    widget = CountrySelect(attrs={"readonly": "readonly", "class": "countryfield"})

    def __init__(self, *args, **kwargs):
        queryset = (
            Country.objects.defer("geom").filter(high_income=False).order_by("name")
        )
        kwargs["queryset"] = queryset

        super(CountryField, self).__init__(*args, **kwargs)


class ActorsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [
            forms.CharField(required=False),
            forms.ChoiceField(choices=kwargs["choices"], required=False),
        ]
        kwargs["widget"] = TextChoiceInput(
            choices=kwargs.pop("choices"),
            help_text=kwargs.pop("help_text", ""),
            attrs={},
        )
        super(ActorsField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value) // 2):
                self.fields.extend(
                    [
                        forms.CharField(required=False),
                        forms.ChoiceField(choices=self.choices, required=False),
                    ]
                )
        return super(ActorsField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list) // 2):
                j = i * 2
                if data_list[j] or data_list[j + 1]:
                    yb_data.append(
                        "%s:%s" % (str(data_list[j] or ""), str(data_list[j + 1] or ""))
                    )
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.CharField(required=False),
                forms.ChoiceField(choices=self.choices, required=False),
            ]
            return ""


class AreaField(forms.MultiValueField):
    """
    MultiValueField for area map with optional shapefile upload.

    Note because of Django's handling of multiple files, compress here
    doesn't do anything with shapefiles, it just returns one (of the several
    required) if there was one.
    """

    def __init__(self, *args, **kwargs):
        fields = (
            MultiPolygonField(required=False, srid="4326", widget=OpenLayersWidget),
            forms.FileField(required=False),
        )
        kwargs.update(
            {"fields": fields, "require_all_fields": False, "widget": AreaWidget}
        )
        super().__init__(*args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Second value (file field) takes precedence
            value = data_list[1] or data_list[0]
        else:
            value = ""

        return value
