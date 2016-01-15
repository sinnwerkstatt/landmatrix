from django.template.context import RequestContext

from global_app.views.deal_detail_view import DealDetailView, get_forms
from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealComparisonView(DealDetailView):

    def dispatch(self, request, *args, **kwargs):
        deal_1 = deal_from_activity_id(kwargs["activity_1_id"])
        deal_2 = deal_from_activity_id(kwargs["activity_2_id"])

        context = super().get_context_data(**kwargs)
        context['deals'] = [ deal_1, deal_2 ]
        context['forms'] = self.get_comparison(deal_1, deal_2)
        print(deal_1)
        print(deal_2)
        return render_to_response('deal-comparison.html', context, RequestContext(request))

    def get_comparison(self, deal_1, deal_2):
        forms_1, forms_2 = get_forms(deal_1), get_forms(deal_2)
        if len(forms_1) != len(forms_2):
            raise IndexError(
                    "Compared deals have different number of forms. Deal id(s): %i, %i. History IDs: %i, %i" %
                    (deal_1.id, deal_2.id, deal_1.activity.history_id, deal_2.activity.history_id)
            )
        comparison_forms = []
        for i in range(len(forms_1)):
            comparison_forms.append((forms_1[i], forms_2[i], is_different(forms_1[i], forms_2[i])))

        return comparison_forms


def deal_from_activity_id(history_id):
    return Deal.from_activity(Activity.history.get(history_id=history_id))


def is_different(form_1, form_2):
    if not isinstance(form_1, form_2.__class__):
        return False

    from random import randint
    return randint(0, 1) == 1
