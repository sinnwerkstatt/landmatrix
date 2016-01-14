from django.template.context import RenderContext

from global_app.views.deal_detail_view import DealDetailView
from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealComparisonView(DealDetailView):

    def dispatch(self, request, *args, **kwargs):
        deal_1 = deal_from_activity_id(kwargs["activity_1_id"])
        deal_2 = deal_from_activity_id(kwargs["activity_2_id"])
        print(deal_1)
        print(deal_2)
        return render_to_response('', {}, RenderContext())


def deal_from_activity_id(history_id):
    return Deal.from_activity(Activity.history.get(history_id=history_id))