from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import BaseFormSet
from django.template.context import RequestContext
from django.views.generic import TemplateView

from grid.views.deal_detail_view import DealDetailView, get_forms
from grid.views.view_aux_functions import render_to_response
from landmatrix.models.activity import HistoricalActivity
from landmatrix.models.deal import Deal
from landmatrix.models.deal_history import DealHistoryItem



class DealComparisonView(TemplateView):

    def dispatch(self, request, activity_1, activity_2=None):
        deal_1 = HistoricalActivity.objects.get(pk=activity_1)
        if activity_2:
            deal_2 = HistoricalActivity.objects.get(pk=activity_2)
        else:
            deal_2 = HistoricalActivity.objects.filter(activity_identifier=deal_1.activity_identifier)\
                .filter(history_date__lt=deal_1.history_date).order_by('history_date').last()
        context = super().get_context_data()
        context['deals'] = [deal_1, deal_2]
        context['forms'] = get_comparison(deal_1, deal_2)
        return render_to_response('deal-comparison.html', context, RequestContext(request))


def get_comparison(deal_1, deal_2):
    forms_1 = get_forms(deal_1)
    forms_2 = get_forms(deal_2)
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
    return Deal.from_activity(HistoricalActivity.objects.get(id=history_id))


#def deal_from_activity_id_and_timestamp(id_and_timestamp):
#    from datetime import datetime
#    from dateutil.tz import tzlocal
#    if '_' in id_and_timestamp:
#        activity_identifier, timestamp = id_and_timestamp.split('_')
#
#        activity = Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()
#        if activity is None:
#            raise ObjectDoesNotExist('activity_identifier %s' % activity_identifier)
#
#        history = activity.history.filter(history_date__lte=datetime.fromtimestamp(float(timestamp), tz=tzlocal())).\
#            filter(fk_status_id__in=(2, 3)).last()
#        if history is None:
#            raise ObjectDoesNotExist('Public deal with activity_identifier %s as of timestamp %s' % (activity_identifier, timestamp))
#
#        return DealHistoryItem.from_activity_with_date(history, datetime.fromtimestamp(float(timestamp), tz=tzlocal()))
#
#    raise RuntimeError('should contain _ separating activity id and timestamp: ' + id_and_timestamp)

def is_different(form_1, form_2):

    if not isinstance(form_1, form_2.__class__):
        return False

    if not form_1.is_valid() == form_2.is_valid():
        return False

    # OMG this is so hacky but I can't help myself
    # Formsets initialized with a list of forms throw a ValidationError:
    # 'ManagementForm data is missing or has been tampered with'
    # Formset initialized with a dict throw a KeyError in _construct_form
    # So I'm replacing _construct_form with my customized version that
    # catches the KeyError here.
    BaseFormSet._construct_form = _construct_form

    if isinstance(form_1, BaseFormSet):
        print(form_1.forms)
        if len(form_1) != len(form_2):
            return False
    else:
        if len(form_1.fields) != len(form_2.fields):
            return False

    for i, field in enumerate(list(form_1)):
        if str(field) != str(list(form_2)[i]):
            return False

    return True


# Hacked version of BaseFormSet._construct_form
def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            # this is the line that has been changed!
            except (IndexError, KeyError):
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form
