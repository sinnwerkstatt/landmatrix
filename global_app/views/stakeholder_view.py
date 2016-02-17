from django.template.context import RequestContext
from django.views.generic.base import TemplateView

from global_app.forms.investor_formset import InvestorForm, InvestorFormSet, ParentStakeholderFormSet
from global_app.views.view_aux_functions import render_to_response


class StakeholderView(TemplateView):

    template_name = 'stakeholder.html'

    def dispatch(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investor_form'] = InvestorForm()
        context['parent_stakeholders'] = ParentStakeholderFormSet()
        context['parent_investors'] = ParentStakeholderFormSet()

        return render_to_response(self.template_name, context, RequestContext(request))

