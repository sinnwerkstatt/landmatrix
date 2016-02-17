from django.core.exceptions import ObjectDoesNotExist

from global_app.forms.investor_formset import InvestorForm
from global_app.forms.parent_stakeholder_formset import ParentStakeholderFormSet
from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.investor import Investor

from django.template.context import RequestContext
from django.views.generic.base import TemplateView


class StakeholderView(TemplateView):

    template_name = 'stakeholder.html'

    def dispatch(self, request, *args, **kwargs):
        print(request, kwargs)
        context = super().get_context_data(**kwargs)
        investor = get_investor(request)
        print(investor)
        context['investor_form'] = InvestorForm(InvestorForm.get_data(investor))
        # context['parent_stakeholders'] = ParentStakeholderFormSet(ParentStakeholderFormSet.get_data(request.POST))
        context['parent_stakeholders'] = ParentStakeholderFormSet()
        # context['parent_investors'] = ParentStakeholderFormSet(ParentStakeholderFormSet.get_data(request.POST))
        context['parent_investors'] = ParentStakeholderFormSet()

        return render_to_response(self.template_name, context, RequestContext(request))


def get_investor(request):
    try:
        return Investor.objects.get(pk=request.GET.get('investor_id', 0))
    except ObjectDoesNotExist:
        return None


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)
