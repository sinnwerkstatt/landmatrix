from django.core.exceptions import ObjectDoesNotExist
from django.template.context import RequestContext

from grid.views.deal_detail_view import DealDetailView, get_forms
from grid.views.view_aux_functions import render_to_response
from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal
from landmatrix.models.deal_history import DealHistoryItem

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealComparisonView(DealDetailView):

    def dispatch(self, request, *args, **kwargs):
#        print('dispatch kwargs:', kwargs)
        activity_1_id = kwargs.get("activity_1_id")
        if activity_1_id is not None:
            deal_1 = deal_from_activity_id(activity_1_id)
            activity_2_id = kwargs.get("activity_2_id")
            if activity_2_id is None:
                raise RuntimeError('Either activity_1_id AND activity_2_id or activity_1 needed. Got ' + str(kwargs))
            deal_2 = deal_from_activity_id(activity_2_id)
        else:
            activity_1 = kwargs.get('activity_1')
            if activity_1 is None:
                raise RuntimeError('Either activity_1_id AND activity_2_id or activity_1 needed. Got ' + str(kwargs))
            deal_1 = deal_from_activity_id_and_timestamp(activity_1)
            deal_2 = previous_history_state(deal_1)

        context = super().get_context_data(**kwargs)
        context['deals'] = [ deal_1, deal_2 ]
        context['forms'] = get_comparison(deal_1, deal_2)

        return render_to_response('deal-comparison.html', context, RequestContext(request))


def get_comparison(deal_1, deal_2):
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
    if history_id.isdigit():
        return Deal.from_activity(Activity.history.get(history_id=history_id))
    raise RuntimeError('Bad activity history id: ' + history_id)


# def deal_from_activity_id_and_timestamp(id_and_timestamp):
#     from datetime import datetime
#     if '_' in id_and_timestamp:
#         activity_identifier, timestamp = id_and_timestamp.split('_')
#
#         activity = Activity.objects.filter(activity_identifier=activity_identifier, fk_status_id__in=(2, 3)).order_by('id').last()
#
#         if activity is None:
#             raise ObjectDoesNotExist('activity_identifier %s' % activity_identifier)
#         history = activity.history.filter(history_date__lte=datetime.fromtimestamp(float(timestamp))).last()
#         if history is None:
#             raise ObjectDoesNotExist('activity_identifier %s, timestamp %s' % (activity_identifier, timestamp))
#
#         return DealHistoryItem.from_activity(history)
#
#     raise RuntimeError('should contain _ separating activity id and timestamp: ' + id_and_timestamp)

def deal_from_activity_id_and_timestamp(id_and_timestamp):
    from datetime import datetime
    from dateutil.tz import tzlocal
    if '_' in id_and_timestamp:
        activity_identifier, timestamp = id_and_timestamp.split('_')

        activity = Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()
        if activity is None:
            raise ObjectDoesNotExist('activity_identifier %s' % activity_identifier)

        history = activity.history.filter(history_date__lte=datetime.fromtimestamp(float(timestamp), tz=tzlocal())).\
            filter(fk_status_id__in=(2, 3)).last()
        if history is None:
            raise ObjectDoesNotExist('Public deal with activity_identifier %s as of timestamp %s' % (activity_identifier, timestamp))

        return DealHistoryItem.from_activity_with_date(history, datetime.fromtimestamp(float(timestamp), tz=tzlocal()))

    raise RuntimeError('should contain _ separating activity id and timestamp: ' + id_and_timestamp)


def previous_history_state(deal):
    from datetime import timedelta
#    print('previous_history_state', deal)
    return Activity.history.filter(id=deal.activity.id).\
        filter(history_date__lte=deal.activity.history_date-timedelta(microseconds=1)).\
        order_by('history_date').last()


def is_different(form_1, form_2):

    if not isinstance(form_1, form_2.__class__):
        return False

    if not form_1.is_valid() == form_2.is_valid():
        return False

    if len(list(form_1)) != len(list(form_2)):
        return False

    for i, field in enumerate(list(form_1)):
        if str(field) != str(list(form_2)[i]):
            return False

    return True