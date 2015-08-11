__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class TitleWidget(forms.TextInput):
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super(TitleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        return "<h3>%s</h3>" % str(self.initial or "")

