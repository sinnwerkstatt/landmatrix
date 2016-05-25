from collections import OrderedDict
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from grid.forms.investor_formset import InvestorForm
from grid.forms.parent_stakeholder_formset import (
    ParentStakeholderFormSet, ParentInvestorFormSet,
)
from landmatrix.models.investor import Investor, InvestorVentureInvolvement


VERBOSE = False


class ChangeStakeholderView(TemplateResponseMixin, BaseDetailView):
    template_name = 'stakeholder.html'
    pk_url_kwarg = 'investor_id'
    context_object_name = 'investor'
    queryset = Investor.objects.all()

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)

        if pk and '_' in pk:
            investor_id, timestamp = pk.split('_')
            investor_date = datetime.datetime.utcfromtimestamp(
                float(timestamp), tzinfo=utc)

            if queryset is None:
                queryset = self.get_queryset()

            try:
                investor = queryset.get(pk=investor_id)
                old_versions = investor.history.filter(
                    history_date__lte=investor_date)
                obj = old_versions.get()
            except queryset.model.DoesNotExist:
                raise Http404(_("No matching stakeholder found."))
        elif pk:
            obj = super().get_object(queryset=queryset)

        return obj

    def get_form(self, form_class, **kwargs):
        if self.request.method == 'POST':
            form = form_class(self.request.POST, **kwargs)
        else:
            form = form_class(**kwargs)

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: move some of this to models.
        involvements_queryset = InvestorVentureInvolvement.objects.filter(
                fk_venture=self.object,
                fk_status__name__in=('pending', 'active', 'overwritten'))
        stakeholders_queryset = involvements_queryset.filter(role='ST')
        investors_queryset = involvements_queryset.filter(role='IN')

        investor_form = self.get_form(InvestorForm, instance=self.object)
        parent_stakeholder_formset = self.get_form(
            ParentStakeholderFormSet, queryset=stakeholders_queryset,
            prefix='parent-stakeholder-form')
        parent_investor_formset = self.get_form(
            ParentInvestorFormSet, queryset=investors_queryset,
            prefix='parent-investor-form')

        try:
            history = get_investor_history(self.object)
        except AttributeError:
            history = None

        context.update({
            'investor_form': investor_form,
            'parent_stakeholders': parent_stakeholder_formset,
            'parent_investors': parent_investor_formset,
            'history': history,
        })

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        investor_form = context['investor_form']
        stakeholders_formset = context['parent_stakeholders']
        investors_formset = context['parent_investors']

        forms = (investor_form, stakeholders_formset, investors_formset)
        if all([form.is_valid() for form in forms]):
            self.object = investor_form.save()

            stakeholders_formset.save(self.object, 'ST')
            investors_formset.save(self.object, 'IN')

        return self.render_to_response(context)


class AddStakeholderView(ChangeStakeholderView):

    def get_object(self, queryset=None):
        return None


def get_investor_history(investor):
    return OrderedDict(reversed(sorted(_investor_history(investor), key=lambda item: item[0])))


def _investor_history(investor):
    date_and_investor = []
    for investor in list(investor.history.all().order_by('history_date')):
        date_and_investor.append((investor.history_date.timestamp(), investor))

    return sorted(date_and_investor, key=lambda entry: entry[0])


# TODO: remove in future. These methods are imported and used elsewhere
# currently however.

def investor_from_id(investor_id):
    try:
        if '_' in investor_id:
            return _investor_from_id_and_timestamp(investor_id)
        else:
            return Investor.objects.get(pk=investor_id)
    except ObjectDoesNotExist:
        return None


def _investor_from_id_and_timestamp(id_and_timestamp):
    from datetime import datetime
    from dateutil.tz import tzlocal
    if '_' in id_and_timestamp:
        investor_id, timestamp = id_and_timestamp.split('_')

        investor = Investor.objects.get(pk=investor_id)

        old_version = investor.history.filter(
            history_date__lte=datetime.fromtimestamp(float(timestamp), tz=tzlocal())
        ).last()
        if old_version is None:
            raise ObjectDoesNotExist('Investor %s as of timestamp %s' % (investor_id, timestamp))

        return old_version

    raise RuntimeError('should contain _ separating investor id and timestamp: ' + id_and_timestamp)
