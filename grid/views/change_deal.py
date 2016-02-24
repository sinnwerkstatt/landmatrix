from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal
from .save_deal_view import SaveDealView, FORMS

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ChangeDealView(SaveDealView):

    template_name = 'change-deal.html'

    def get_activity(self, **kwargs):
        return Activity.objects.get(activity_identifier=kwargs.get('deal_id'))

    def get_forms(self, data=None):
        return [get_form(Deal(self.activity.activity_identifier), form) for form in FORMS]


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)
