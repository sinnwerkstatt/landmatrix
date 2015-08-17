__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class NumberInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({'type': 'number'})
        return super(NumberInput, self).render(name, value, attrs)
