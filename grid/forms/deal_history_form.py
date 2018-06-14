from django.utils.translation import ugettext_lazy as _

from .base_form import BaseForm


class DealHistoryForm(BaseForm):
    '''
    Apparently this is a placeholder form for history,
    which is read only.
    '''
    form_title = _('Deal history')

    class Meta:
        name = 'history'
