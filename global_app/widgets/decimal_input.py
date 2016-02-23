__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class DecimalInput(forms.TextInput):
    def render(self, name, value, attrs={}):
        attrs.update({
            'type': 'number',
            'step': 'any',
            'class': 'form-control'
        })
        return super(DecimalInput, self).render(name, value, attrs)
