__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .title_widget import TitleWidget

from django import forms


class TitleField(forms.CharField):
    '''
    TODO: default to required=False and label="" (repeated everywhere)
    '''
    widget = forms.HiddenInput
    is_title = True

    def __init__(self, *args, **kwargs):
        self.widget = TitleWidget(initial=kwargs.get("initial"))
        super().__init__(*args, **kwargs)
