from django.template.context import RequestContext
from django.views.generic.base import TemplateView

from global_app.forms.investor_formset import InvestorForm
from global_app.forms.parent_stakeholder_formset import ParentStakeholderFormSet
from global_app.views.view_aux_functions import render_to_response


class StakeholderView(TemplateView):

    template_name = 'stakeholder.html'

    def dispatch(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investor_form'] = InvestorForm(InvestorForm.get_data(request.POST))
        # context['parent_stakeholders'] = ParentStakeholderFormSet(ParentStakeholderFormSet.get_data(request.POST))
        context['parent_stakeholders'] = ParentStakeholderFormSet()
        # context['parent_investors'] = ParentStakeholderFormSet(ParentStakeholderFormSet.get_data(request.POST))
        context['parent_investors'] = ParentStakeholderFormSet()

        return render_to_response(self.template_name, context, RequestContext(request))

def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)
