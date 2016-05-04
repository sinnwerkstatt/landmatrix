from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country
from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, NumberInput


def get_country_specific_form_class(deal, data=None, files=None):
    target_country_slug = _get_deal_target_country_slug(deal)

    try:
        form_class = COUNTRY_FORMS[target_country_slug]
    except KeyError:
        return None
    else:
        return form_class


def _get_deal_target_country_slug(deal):
    # TODO: move to models, once I understand things a bit better
    try:
        target_country_name = deal.attributes['target_country']
    except (KeyError, AttributeError):
        pass
    else:
        try:
            target_country = Country.objects.get(name=target_country_name)
        except Country.DoesNotExist:
            pass
        else:
            return target_country.slug

    return None


class GermanyForm(BaseForm):
    form_title = _('Germany')
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(required=False,
                                       label=_("Intended size"),
                                       help_text=_("ha"), widget=NumberInput)
    test_integer = forms.IntegerField(required=False,
                                      label=_("Test integer"),
                                      widget=NumberInput)

    class Meta:
        name = 'germany specific info'


COUNTRY_FORMS = {
    'germany': GermanyForm,
}
