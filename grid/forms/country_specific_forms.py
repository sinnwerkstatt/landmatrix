from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.forms.base_form import BaseForm
from grid.fields import TitleField
from grid.widgets import NumberInput


def get_country_specific_form_classes(activity, data=None, files=None):
    try:
        slug = activity.target_country.slug
    except AttributeError:
        form_class = None
    else:
        form_class = COUNTRY_SPECIFIC_FORMS.get(slug, None)

    if form_class:
        return [form_class]
    else:
        return []


class MongoliaForm(BaseForm):
    """
    This is just a simple example.
    """
    form_title = _('Mongolia')
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(
        required=False, label=_("Intended size"), help_text=_("ha"),
        widget=NumberInput)
    test_integer = forms.IntegerField(
        required=False, label=_("Test integer"), widget=NumberInput)

    class Meta:
        name = 'mongolia specific info'


COUNTRY_SPECIFIC_FORMS = {
    'mongolia': MongoliaForm,
}
