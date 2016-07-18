import datetime
from dateutil.tz import tzlocal

from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import BaseFormSet
from django.template.context import RequestContext
from django.views.generic.base import TemplateView

from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.views.view_aux_functions import render_to_response
from landmatrix.models.investor import Investor


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorComparisonView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        investor_1_id = kwargs.pop('investor_1', None)
        if investor_1_id is None:
            raise RuntimeError('investor_1 needed. Got ' + str(kwargs))
        if '_' in investor_1_id:
            investor_1 = _investor_from_id_and_timestamp(investor_1_id)
        else:
            investor_1 = Investor.objects.get(pk=investor_1_id).history.last()
        investor_2 = previous_history_state(investor_1)
        context = super().get_context_data(**kwargs)
        context['investors'] = [investor_1, investor_2]
        context['comparison_forms'] = get_comparison(investor_1, investor_2)

        return render_to_response(
            'investor-comparison.html', context, RequestContext(request))


def investor_from_historical(old_version):
    if old_version is None:
        return None
    return {
        'investor_identifier': old_version.investor_identifier,
        'name': old_version.name,
        'fk_country': old_version.fk_country,
        'classification': old_version.classification,
        'homepage': old_version.homepage,
        'opencorporates_link': old_version.opencorporates_link,
        'comment': old_version.comment,
        'fk_status': old_version.fk_status,
        'timestamp': old_version.timestamp,
    }


def get_comparison(investor_1, investor_2):
    form_1 = get_form(investor_1)
    form_2 = get_form(investor_2)
    return (form_1, form_2, is_different(form_1, form_2))


def get_form(investor):
    return OperationalStakeholderForm(initial=investor_from_historical(investor))


def previous_history_state(investor):
    from datetime import timedelta
    old_version = Investor.history.filter(id=investor.id).\
        filter(history_date__lte=investor.history_date - timedelta(microseconds=1)).\
        order_by('history_date').last()
    return old_version

def is_different(form_1, form_2):

    if not form_1.is_valid() == form_2.is_valid():
        return False

    # OMG this is so hacky but I can't help myself
    # Formsets initialized with a list of forms throw a ValidationError:
    # 'ManagementForm data is missing or has been tampered with'
    # Formset initialized with a dict throw a KeyError in _construct_form
    # So I'm replacing _construct_form with my customized version that
    # catches the KeyError here.
    BaseFormSet._construct_form = _construct_form

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


def investor_from_id(investor_id):
    try:
        if '_' in investor_id:
            return _investor_from_id_and_timestamp(investor_id)
        else:
            return Investor.objects.get(pk=investor_id)
    except ObjectDoesNotExist:
        return None


def _investor_from_id_and_timestamp(id_and_timestamp):
    if '_' not in id_and_timestamp:
        message = 'should contain _ separating investor id and timestamp: {}'.format(id_and_timestamp)
        raise ValueError(message)

    investor_id, timestamp = id_and_timestamp.split('_')

    investor = Investor.objects.get(pk=investor_id)

    history_date = datetime.datetime.fromtimestamp(
        float(timestamp), tz=tzlocal())
    old_version = investor.history.filter(
        history_date__lte=history_date).last()
    if old_version is None:
        raise ObjectDoesNotExist('Investor %s as of timestamp %s' % (investor_id, timestamp))

    return old_version
