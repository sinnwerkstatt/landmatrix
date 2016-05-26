from django.utils.translation import ugettext_lazy as _
from django import forms

from landmatrix.models.investor import Investor
from landmatrix.models.status import Status
from grid.forms.base_model_form import BaseModelForm
from grid.widgets import CommentInput


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


# Change this to a livesearch widget once you got a working one
class InvestorField(forms.ChoiceField):
    def widget_attrs(self, widget):
        return {'class': 'investorfield'}


class InvestorForm(BaseModelForm):
    name = forms.CharField(required=False, label=_("Name"), max_length=255)
    tg_general_comment = forms.CharField(required=False,
                                         label=_("Additional comments"),
                                         widget=CommentInput)

    class Meta:
        model = Investor
        fields = ['name', 'fk_country', 'classification', 'tg_general_comment']

    def save(self, commit=True):
        '''
        Force status to pending on update.
        '''
        instance = super().save(commit=False)
        instance.fk_status = Status.objects.get(name='pending')
        if commit:
            instance.save()

        return instance

    def get_attributes(self, **kwargs):
        '''
        Attempt to copy the BaseForm API here.
        '''
        return {
            'comment': self.cleaned_data.get('tg_general_comment'),
        }

    @classmethod
    def get_data(cls, investor):
        '''
        Attempt to copy the BaseForm API here.
        '''
        return {}
