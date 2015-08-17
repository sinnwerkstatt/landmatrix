__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.widgets.country_select import CountrySelect
from landmatrix.models.country import Country

from django import forms


class CountryField(forms.ModelChoiceField):

    widget = CountrySelect(attrs={"readonly":"readonly"})

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Country.objects.all().order_by("name")
        super(CountryField, self).__init__(*args, **kwargs)
