from django import forms

from apps.grid.forms.base_form import FieldsDisplayFormMixin


class BaseModelForm(forms.ModelForm, FieldsDisplayFormMixin):

    pass
