from django import forms
from django.forms.formsets import formset_factory

from landmatrix.models.browse_condition import BrowseCondition


class BrowseConditionForm(forms.ModelForm):
    class Meta:
        model = BrowseCondition
        exclude = ('rule',)

ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
