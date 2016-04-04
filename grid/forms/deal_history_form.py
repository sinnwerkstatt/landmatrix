__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm

from django.utils.translation import ugettext_lazy as _


class DealHistoryForm(BaseForm):
    form_title = _('Deal history')

    class Meta:
    	name = 'history'