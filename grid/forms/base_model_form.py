from django import forms
from grid.forms.base_form import FieldsDisplayFormMixin


class BaseModelForm(forms.ModelForm,
                    FieldsDisplayFormMixin):

    pass
