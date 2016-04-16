from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country
from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, NumberInput


def get_country_specific_form(deal, data=None, files=None):
    # TODO: move country finding to models
    form = None

    try:
        target_country = deal.attributes['target_country']
    except (KeyError, AttributeError):
        pass
    else:
        country = Country.objects.get(name=target_country)
        try:
            form_cls = COUNTRY_FORMS[country.slug]
        except KeyError:
            pass
        else:
            form = form_cls(data, files=files)

    return form


class GermanyForm(BaseForm):
    form_title = _('Germany')
    tg_land_area = TitleField(required=False, label="", initial=_("Land area"))
    intended_size = forms.IntegerField(required=False,
                                       label=_("Intended size"),
                                       help_text=_("ha"), widget=NumberInput)


COUNTRY_FORMS = {
    'germany': GermanyForm,
}
