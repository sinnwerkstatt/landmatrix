from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Country, ActivityAttributeGroup
from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, NumberInput


def get_country_specific_form_classes(activity, data=None, files=None):
    for target_country_slug in _get_deal_target_country_slugs(activity):
        try:
            form_class = COUNTRY_FORMS[target_country_slug]
        except KeyError:
            pass
        else:
            yield form_class


def _get_deal_target_country_slugs(activity):
    # Activity may also be an ActivityHistory instance
    # (from django-simple-history) hence the weird query below.
    # TODO: move to models, once I understand things a bit better
    attr_groups = ActivityAttributeGroup.objects.filter(
        fk_activity_id=activity.id)
    attr_groups = attr_groups.filter(attributes__contains='target_country')

    for attr_group in attr_groups:
        target_country_id = attr_group.attributes['target_country']
        try:
            target_country = Country.objects.get(id=target_country_id)
        except Country.DoesNotExist:
            pass
        else:
            yield target_country.slug


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
