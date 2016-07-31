from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country, ActivityAttribute
from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, NumberInput


def get_country_specific_form_classes(activity, data=None, files=None):
    try:
        form_class = COUNTRY_SPECIFIC_FORMS.get(activity.target_country.slug, None)
    except:
        return []
    if form_class:
        return [form_class]
    else:
        return []

class GermanyForm(BaseForm):
    '''
    This is just a simple example.
    '''
    form_title = _('Germany')
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(
        required=False, label=_("Intended size"), help_text=_("ha"),
        widget=NumberInput)
    test_integer = forms.IntegerField(
        required=False, label=_("Test integer"), widget=NumberInput)

    class Meta:
        name = 'germany specific info'


COUNTRY_SPECIFIC_FORMS = {
    #'germany': GermanyForm,
}
