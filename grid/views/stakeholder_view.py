from pprint import pprint

from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist

from grid.forms.investor_formset import InvestorForm
from grid.forms.parent_stakeholder_formset import ParentStakeholderFormSet, ParentInvestorFormSet
from grid.views.view_aux_functions import render_to_response
from landmatrix.models.investor import Investor, InvestorVentureInvolvement

from django.template.context import RequestContext
from django.views.generic.base import TemplateView

from landmatrix.models.status import Status


VERBOSE = False


class StakeholderView(TemplateView):

    template_name = 'stakeholder.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            investor = investor_from_id(kwargs["investor_id"])
        except KeyError:
            investor = None

        context = super(StakeholderView, self).get_context_data(**kwargs)
        context['investor'] = investor
        context['investor_form'] = InvestorForm(InvestorForm.get_data(investor))
        context['parent_stakeholders'] = ParentStakeholderFormSet(initial=ParentStakeholderFormSet.get_data(investor, role='ST'), prefix='parent-stakeholder-form')
        context['parent_investors'] = ParentInvestorFormSet(initial=ParentInvestorFormSet.get_data(investor, role='IN'), prefix='parent-investor-form')
        try:
            context['history'] = get_investor_history(investor)
        except AttributeError:
            pass

        if request.POST:
            save_from_post(request.POST)

        return render_to_response(self.template_name, context, RequestContext(request))


def save_from_post(POST):
    investor = investor_from_id(POST['investor'])
    if not investor:
        return

    save_investor_changes(investor, POST)
    save_involvement_changes(investor, POST)


def extract_formset_data(POST):
    return {key: POST[key] for key in POST.keys() if key.startswith('form-') and not key[5].istitle()}


def save_investor_changes(investor, POST):
    investor_form = InvestorForm(POST)
    if investor_form.is_valid():
        classification = investor_form.cleaned_data['classification']
        investor_name = investor_form.cleaned_data['investor_name']
        country_id = investor_form.cleaned_data['country']
        if investor_name != investor.name:
            investor.name = investor_name
        if classification != investor.classification:
            investor.classification = classification
        if investor.fk_country_id != country_id:
            investor.fk_country_id = country_id

        investor.save()
        # TODO create changeset


def save_involvement_changes(investor, POST):
    stakeholder_data = get_separate_form_data(extract_formset_data(POST))

    delete_involvements_removed_in_frontend(investor, stakeholder_data)

    involvements = get_active_involvements(investor)

    for stakeholder in stakeholder_data:
        corresponding_involvements = involvements.filter(fk_investor_id=stakeholder['stakeholder'])
        if not len(corresponding_involvements):
            if VERBOSE:
                print('CREATING involvement for ', stakeholder, ', not in', [i.id for i in involvements])
            InvestorVentureInvolvement.objects.create(
                fk_venture=investor, fk_investor_id=stakeholder['stakeholder'], percentage=stakeholder['percentage'],
                fk_status=Status.objects.get(name='pending')
            )
        else:
            for involvement in corresponding_involvements:
                if VERBOSE:
                    print(
                        'UPDATING stakeholder %i percentage from %f to %f' % (
                            involvement.id, float(involvement.percentage), float(stakeholder['percentage'])
                        )
                    )
                involvement.percentage = stakeholder['percentage']
                involvement.fk_status = Status.objects.get(name='pending')
                involvement.save()

    # TODO create changeset


def delete_involvements_removed_in_frontend(investor, stakeholder_data):
    involvements = get_active_involvements(investor)
    for involvement in involvements:
        if int(involvement.fk_investor_id) not in [int(stakeholder['stakeholder']) for stakeholder in stakeholder_data]:
            if VERBOSE:
                print('DELETING |', str(involvement)[:51], '|, not in', stakeholder_data)
            involvement.fk_status = Status.objects.get(name='deleted')
            involvement.save()
    # TODO create changeset


def get_active_involvements(investor):
    return InvestorVentureInvolvement.objects.filter(fk_venture=investor). \
        filter(fk_status__name__in=('pending', 'active', 'overwritten'))


def get_separate_form_data(formset_post):
    # in:  { form-0-key: value, form-1-key: value }
    # out: [{key: value}, {key: value}]
    i = 0
    out = []
    while True:
        valid_keys = [key for key in formset_post.keys() if key.startswith('form-%i' % i)]
        if not valid_keys:
            return out
        form_data = {key.replace('form-%i-' % i, ''): formset_post[key] for key in valid_keys}
        out.append(form_data)
        i += 1
        if i > 1000:
            return out


def get_investor(request):
    return investor_from_id(request.GET.get('investor_id', 0))


def investor_from_id(investor_id):
    try:
        if '_' in investor_id:
            return _investor_from_id_and_timestamp(investor_id)
        else:
            return Investor.objects.get(pk=investor_id)
    except ObjectDoesNotExist:
        return None


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)


def get_investor_history(investor):
    return OrderedDict(reversed(sorted(_investor_history(investor), key=lambda item: item[0])))


def _investor_history(investor):
    date_and_investor = []
    for investor in list(investor.history.all().order_by('history_date')):
        date_and_investor.append((investor.history_date.timestamp(), investor))

    return sorted(date_and_investor, key=lambda entry: entry[0])


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
