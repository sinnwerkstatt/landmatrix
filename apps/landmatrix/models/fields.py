from django import forms
from django.contrib.postgres.fields import ArrayField as _ArrayField
from django.core.validators import RegexValidator
from django.db.models import CharField, DecimalField

loose_date_re_val = RegexValidator(
    regex=r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
    message="Use yyyy or yyyy-mm or yyyy-mm-dd",
    code="invalid_date",
)


class LooseDateField(CharField):
    default_validators = [loose_date_re_val]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super().__init__(*args, **kwargs)


class NanoIDField(CharField):
    pass


# NOTE: Not in use, but referenced by migrations
# TODO: Delete after squashing migrations
class DecimalIntField(DecimalField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return float(value)


class ArrayField(_ArrayField):
    def value_to_string(self, obj):
        return self.value_from_object(obj)


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 4.2's postgres ArrayField
    and a TypeMultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(
            models.CharField(max_length=..., choices=(...,)), blank=[...], default=[...]
        )
    """

    class _TypedMultipleChoiceField(forms.TypedMultipleChoiceField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("base_field", None)
            kwargs.pop("max_length", None)
            super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self._TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class ChoiceField(CharField):
    def __init__(self, choices, *args, **kwargs):
        if not choices:
            raise ValueError("The 'choices' argument is required and cannot be empty.")

        kwargs["choices"] = choices
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)

        super().__init__(*args, **kwargs)
