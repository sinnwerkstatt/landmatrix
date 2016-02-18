from django.core.exceptions import ObjectDoesNotExist

from global_app.forms.investor_formset import InvestorForm
from global_app.forms.parent_stakeholder_formset import ParentStakeholderFormSet, ParentInvestorFormSet
from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.investor import Investor, InvestorVentureInvolvement

from django.template.context import RequestContext
from django.views.generic.base import TemplateView

from landmatrix.models.status import Status


class StakeholderView(TemplateView):

    template_name = 'stakeholder.html'

    def dispatch(self, request, *args, **kwargs):
        print('dispatch')
        context = super().get_context_data(**kwargs)
        investor = get_investor(request)
        context['investor_form'] = InvestorForm(InvestorForm.get_data(investor))
        context['parent_stakeholders'] = ParentStakeholderFormSet(initial=ParentStakeholderFormSet.get_data(investor, role='ST'))
        context['parent_investors'] = ParentInvestorFormSet(initial=ParentInvestorFormSet.get_data(investor, role='IN'))

        if request.POST:
            save_from_post(request.POST)

        return render_to_response(self.template_name, context, RequestContext(request))


def save_from_post(POST):
    print('POST:', POST)
    investor = investor_from_id(POST['investor'])
    if not investor:
        return
    investor_form = InvestorForm(POST)

    print('investor_form.is_valid', investor_form.is_valid())
    print('investor_form.cleaned_data',investor_form.cleaned_data)

    classification = investor_form.cleaned_data['classification']
    investor_name = investor_form.cleaned_data['investor_name']
    country_id =  investor_form.cleaned_data['country']

    formset_post = {key: POST[key] for key in POST.keys() if key.startswith('form-') and not key[5].istitle()}
    print(formset_post)
    stakeholder_data = get_separate_form_data(formset_post)

    # stakeholder_formset = ParentStakeholderFormSet(POST)
    #
    # print('stakeholder_formset.is_valid', stakeholder_formset.is_valid())
    # print('stakeholder_formset.cleaned_data', stakeholder_formset.cleaned_data)

    if investor_name != investor.name:
        investor.name = investor_name
        print(investor_name)
    if classification != investor.classification:
        investor.classification = classification
        print(classification)
    if investor.fk_country_id != country_id:
        investor.fk_country_id = country_id
        print(country_id)

    involvements = InvestorVentureInvolvement.objects.filter(fk_venture=investor)
    for involvement in involvements:
        if involvement.fk_investor_id not in [stakeholder['stakeholder'] for stakeholder in stakeholder_data]:
            print(str(involvement)[:51], 'not in', stakeholder_data)
            involvement.delete()
            continue
    for stakeholder in stakeholder_data:
        corresponding_involvements = InvestorVentureInvolvement.objects.filter(fk_venture=investor).\
            filter(fk_investor_id=stakeholder['stakeholder'])
        if not len(corresponding_involvements):
            print(stakeholder, 'not in', [i.id for i in involvements])
            InvestorVentureInvolvement.objects.create(
                fk_venture=investor, fk_investor_id=stakeholder['stakeholder'], percentage=stakeholder['percentage'],
                fk_status=Status.objects.get(name='pending')
            )
        else:
            for involvement in corresponding_involvements:
                print('updating stakeholder %i percentage from %f to %f' % (involvement.id, involvement.percentage, stakeholder['percentage']))
                involvement.percentage = stakeholder['percentage']
                involvement.fk_status=Status.objects.get(name='pending')
                involvement.save()
    # TODO create changeset


def get_separate_form_data(formset_post):
    # in:  { form-0-key: value, form-1-key: value }
    # out: [{key: value}, {key: value}
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


def investor_from_id(id):
    try:
        return Investor.objects.get(pk=id)
    except ObjectDoesNotExist:
        return None


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)
