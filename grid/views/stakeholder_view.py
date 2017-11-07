from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from grid.forms.investor_form import ParentInvestorForm, ParentStakeholderForm, OperationalCompanyForm
from grid.forms.parent_investor_formset import (
    ParentCompanyFormSet, ParentInvestorFormSet,
)
from landmatrix.models.investor import Investor, InvestorVentureInvolvement


class InvestorFormsMixin:
    '''
    Handle the shared form behaviour for create and update.
    '''

    def get_form_class(self):
        investor = self.get_object()
        # Check current role of investor
        role = self.request.GET.get('role', '')
        if not role:
            if investor and investor.is_operating_company:
                role = 'operational_stakeholder'
            else:
                role = 'parent_investor'
        if role == 'parent_investor':
            return ParentInvestorForm
        elif role == 'parent_company':
            return ParentStakeholderForm
        else:
            return OperationalCompanyForm

    def get_formset_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_venture_involvements_queryset(self):
        if self.object:
            queryset = self.object.venture_involvements.active()
        else:
            queryset = InvestorVentureInvolvement.objects.none()
        queryset = queryset.order_by('fk_investor__name')

        return queryset

    def get_stakeholders_formset_kwargs(self):
        kwargs = self.get_formset_kwargs()
        kwargs['prefix'] = 'parent-company-form'

        queryset = self.get_venture_involvements_queryset().filter(role=InvestorVentureInvolvement.STAKEHOLDER_ROLE)
        kwargs['queryset'] = queryset

        return kwargs

    def get_investors_formset_kwargs(self):
        kwargs = self.get_formset_kwargs()
        kwargs['prefix'] = 'parent-investor-form'

        queryset = self.get_venture_involvements_queryset().filter(role=InvestorVentureInvolvement.INVESTOR_ROLE)
        kwargs['queryset'] = queryset

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = self.get_form(form_class=self.get_form_class())

        if 'parent_companies' not in context:
            stakeholders_kwargs = self.get_stakeholders_formset_kwargs()
            context['parent_companies'] = ParentCompanyFormSet(
                **stakeholders_kwargs)

        if 'parent_investors' not in context:
            investors_kwargs = self.get_investors_formset_kwargs()
            context['parent_investors'] = ParentInvestorFormSet(
                **investors_kwargs)

        role = self.request.GET.get('role', None)
        if not role:
            # Guess role
            investor = self.get_object()
            if investor and investor.is_operating_company:
                context['role'] = 'operational_stakeholder'
            else:
                context['role'] = 'parent_investor'
        ROLE_MAP = {
            'operational_stakeholder': _('Operating company'),
            'parent_company': _('Parent company'),
            'parent_investor': _('Tertiary investor/lender'),
        }
        context['role'] = ROLE_MAP.get(role, _('Operating company'))
        return context

    def form_invalid(self, investor_form, stakeholders_formset,
                     investors_formset):
        context = self.get_context_data(
            form=investor_form, parent_companies=stakeholders_formset,
            parent_investors=investors_formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        '''
        Override standard post behaviour to check all three forms.
        '''
        self.object = self.get_object()

        stakeholders_formset_kwargs = self.get_stakeholders_formset_kwargs()
        investors_formset_kwargs = self.get_investors_formset_kwargs()

        investor_form = self.get_form()
        stakeholders_formset = ParentCompanyFormSet(
            **stakeholders_formset_kwargs)
        investors_formset = ParentInvestorFormSet(**investors_formset_kwargs)

        forms = (investor_form, stakeholders_formset, investors_formset)

        if all([form.is_valid() for form in forms]):
            response = self.form_valid(investor_form, stakeholders_formset,
                                       investors_formset)
        else:
            response = self.form_invalid(investor_form, stakeholders_formset,
                                         investors_formset)

        return response


class ChangeStakeholderView(InvestorFormsMixin, UpdateView):
    template_name = 'stakeholder.html'
    context_object_name = 'investor'
    model = Investor

    def get_object(self):
        # TODO: Cache result for user
        investor_id = self.kwargs.get('investor_id')
        history_id = self.kwargs.get('history_id')
        try:
            if history_id:
                investor = Investor.objects.get(id=history_id)
            else:
                investor = Investor.objects.get(investor_identifier=investor_id)
        except Investor.DoesNotExist as e:
            raise Http404('Investor %s does not exist (%s)' % (investor_id, str(e)))
        except Investor.MultipleObjectsReturned as e:
            # Get latest (this shouldn't happen though)
            investor = Investor.objects.filter(investor_identifier=investor_id).order_by('-id').first()

        can_change = self.request.user.has_perm('landmatrix.change_investor')
        if investor.is_deleted and not can_change:
            raise Http404('Investor %s has been deleted' % investor_id)

        return investor

    def form_valid(self, investor_form, stakeholders_formset,
                   investors_formset):
        self.object = investor_form.save()
        stakeholders_formset.save(self.object)
        investors_formset.save(self.object)

        # Is dialog?
        if self.request.GET.get('popup', False):
            response = self.render_popup()
        else:
            context = self.get_context_data(
                form=investor_form, parent_companies=stakeholders_formset,
                parent_investors=investors_formset)
            response = self.render_to_response(context)

        return response

    def render_popup(self):
        result = """
        <script type="text/javascript">
        opener.dismissChangeInvestorPopup(window, '%s', '%s')
        </script>
        """ % (
            escape(self.object.id),
            escape(self.object.name)
        )
        return HttpResponse(result)


class AddStakeholderView(InvestorFormsMixin, CreateView):
    model = Investor
    form_class = ParentInvestorForm
    template_name = 'stakeholder.html'
    context_object_name = 'investor'

    def get_success_url(self):
        return reverse_lazy(
            'stakeholder_form', kwargs={'investor_id': self.object.pk})

    def get_object(self):
        return None

    def get_stakeholders_formset_kwargs(self):
        kwargs = super().get_stakeholders_formset_kwargs()

        parent_id = self.request.GET.get('parent_id', False)
        if parent_id:
            parent_initial = {'fk_investor': parent_id}
            if 'initial' not in kwargs:
                kwargs['initial'] = []
            kwargs['initial'].append(parent_initial)

        return kwargs

    def render_popup(self):
        result = """
        <script type="text/javascript">
        opener.dismissAddInvestorPopup(window, '%s', '%s')
        </script>
        """ % (
            escape(self.object.id),
            escape(self.object.name)
        )
        return HttpResponse(result)

    def form_valid(self, investor_form, stakeholders_formset,
                   investors_formset):
        self.object = investor_form.save()
        stakeholders_formset.save(self.object)
        investors_formset.save(self.object)

        # Is dialog?
        if self.request.GET.get('popup', False):
            response = self.render_popup()
        else:
            response = HttpResponseRedirect(self.get_success_url())

        return response
