from django import forms

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TitleWidget(forms.TextInput):
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        return "<h3>%s</h3>" % str(self.initial or "")

