__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms

from grid.widgets.year_based_widget import YearBasedWidget

class YearBasedCheckboxInput(forms.MultiWidget):
    widget = forms.CheckboxInput(attrs={"class": "year-based"})