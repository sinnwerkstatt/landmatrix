__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms

from grid.widgets.year_based_widget import YearBasedWidget

class YearBasedCheckboxInput(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.widget = forms.CheckboxInput(attrs={"class": "year-based"})
        super().__init__(*args, **kwargs)