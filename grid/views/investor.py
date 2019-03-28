from datetime import datetime

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView, DetailView

from api.filters import Filter
from grid.forms.investor_form import ParentInvestorForm, ParentStakeholderForm, OperationalCompanyForm
from grid.forms.parent_investor_formset import ParentCompanyFormSet, ParentInvestorFormSet
from grid.views.base import TableGroupView
from grid.views.filter import get_investor_variable_table
from grid.views.browse_filter_conditions import get_investor_field_label
from grid.utils import has_perm_approve_reject
from landmatrix.models.investor import InvestorBase, Investor, HistoricalInvestor, HistoricalInvestorVentureInvolvement


class InvestorFormsMixin:
    """
    Handle the shared form behaviour for create and update.
    """
    def get_form_class(self):
        hinvestor = self.get_object()
        # Check current role of investor
        role = self.request.GET.get('role', '')
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
            queryset = self.object.venture_involvements.all()
        else:
            queryset = HistoricalInvestorVentureInvolvement.objects.none()
        queryset = queryset.order_by('fk_investor__name')

        return queryset

    def get_stakeholders_formset_kwargs(self):
        kwargs = self.get_formset_kwargs()
        kwargs['prefix'] = 'parent-company-form'

        queryset = self.get_venture_involvements_queryset().filter(
            role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE)
        kwargs['queryset'] = queryset

        return kwargs

    def get_investors_formset_kwargs(self):
        kwargs = self.get_formset_kwargs()
        kwargs['prefix'] = 'parent-investor-form'

        queryset = self.get_venture_involvements_queryset().filter(
            role=HistoricalInvestorVentureInvolvement.INVESTOR_ROLE)
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
            hinvestor = self.get_object()
            if hinvestor and hinvestor.is_operating_company:
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
        stakeholders_formset = ParentCompanyFormSet(**stakeholders_formset_kwargs)
        investors_formset = ParentInvestorFormSet(**investors_formset_kwargs)

        forms = (investor_form, stakeholders_formset, investors_formset)

        if all([form.is_valid() for form in forms]):
            response = self.form_valid(investor_form, stakeholders_formset, investors_formset)
        else:
            response = self.form_invalid(investor_form, stakeholders_formset, investors_formset)

        return response


class InvestorUpdateView(InvestorFormsMixin,
                         UpdateView):

    template_name = 'grid/investor_form.html'
    context_object_name = 'investor'
    model = HistoricalInvestor
    success_message = _('Your changes to the investor have been submitted successfully. The changes will be reviewed and published soon.')
    success_message_admin = _('Your changes to the investor have been saved successfully.')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        # TODO: Cache result for user
        investor_id = self.kwargs.get('investor_id')
        history_id = self.kwargs.get('history_id')
        queryset = HistoricalInvestor.objects
        try:
            if history_id:
                investor = queryset.get(id=history_id)
            else:
                investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Investor %s does not exist (%s)' % (investor_id, str(e)))
        # Reporters are allowed to change only investors they've created
        #user = self.request.user
        #if user.groups.filter(name='Reporters').count() > 0:
        #    if investor.history_user != user:
        #        raise Http404('You are not allowed to edit investor %s' % investor_id)
        return investor

    def form_valid(self, investor_form, stakeholders_formset, investors_formset):
        old_hinvestor = self.get_object()
        is_admin = self.request.user.has_perm('landmatrix.change_investor')
        is_editor = self.request.user.has_perm('landmatrix.review_investor')

        if old_hinvestor.fk_status_id == HistoricalInvestor.STATUS_PENDING:
            # Only editors and administrators are allowed to edit pending versions
            if not is_editor and not is_admin:
                return HttpResponseForbidden('Investor version is pending')

        # Don't create new version if rejected
        if 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, old_hinvestor):
            hinvestor = old_hinvestor
        else:
            hinvestor = investor_form.save(user=self.request.user)
            stakeholders_formset.save(hinvestor)
            investors_formset.save(hinvestor)

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hinvestor):
            messages.success(self.request, self.success_message_admin.format(hinvestor.investor_identifier))
            hinvestor.approve_change(self.request.user, hinvestor.comment)
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hinvestor):
            hinvestor.reject_change(self.request.user, hinvestor.comment)
        else:
            messages.success(self.request, self.success_message.format(hinvestor.investor_identifier))

        # Is dialog?
        self.object = hinvestor
        if self.request.GET.get('popup', False):
            return self.render_popup()

        return redirect('investor_detail', investor_id=hinvestor.investor_identifier)

    def render_popup(self):
        result = """
        <script type="text/javascript">
        opener.dismissChangeInvestorPopup(window, '%s', '%s', '%s')
        </script>
        """ % (
            escape(self.object.id),
            escape(self.object.name),
            escape(self.object.investor_identifier),
        )
        return HttpResponse(result)


class InvestorCreateView(InvestorFormsMixin,
                         CreateView):

    model = HistoricalInvestor
    template_name = 'grid/investor_form.html'
    context_object_name = 'investor'
    success_message = _('The investor has been submitted successfully (#{}). It will be reviewed and published soon.')
    success_message_admin = _('The investor has been added successfully (#{}).')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'investor_update', kwargs={'investor_id': self.object.investor_identifier})

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
        opener.dismissAddInvestorPopup(window, '%s', '%s', '%s')
        </script>
        """ % (
            escape(self.object.id),
            escape(self.object.name),
            escape(self.object.investor_identifier)
        )
        return HttpResponse(result)

    def form_valid(self, investor_form, stakeholders_formset, investors_formset):
        hinvestor = investor_form.save(user=self.request.user)
        stakeholders_formset.save(self.object)
        investors_formset.save(self.object)

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hinvestor):
            messages.success(self.request, self.success_message_admin.format(hinvestor.investor_identifier))
            hinvestor.approve_change(self.request.user, hinvestor.comment)
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hinvestor):
            hinvestor.reject_change(self.request.user, hinvestor.comment)
        else:
            messages.success(self.request, self.success_message.format(hinvestor.investor_identifier))

        # Is dialog?
        self.object = hinvestor
        if self.request.GET.get('popup', False):
            response = self.render_popup()
        else:
            response = HttpResponseRedirect(self.get_success_url())

        return response


class InvestorDetailView(DetailView):

    model = HistoricalInvestor
    template_name = "grid/investor_detail.html"
    context_object_name = "investor"

    def get_object(self):
        # TODO: Cache result for user
        investor_id = self.kwargs.get('investor_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalInvestor.objects
        if not self.request.user.is_authenticated():
            i = self._get_public_investor()
            if not i:
                raise Http404('Investor %s is not public' % investor_id)
            queryset = queryset.public_or_deleted(self.request.user)
        try:
            if history_id:
                investor = queryset.get(id=history_id)
            else:
                investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (investor_id, str(e)))
        # Status: Deleted
        if investor.fk_status_id == HistoricalInvestor.STATUS_DELETED:
            # Only Administrators are allowed to edit (recover) deleted deals
            if not self.request.user.has_perm('landmatrix.change_investor'):
                raise Http404('Investor %s has been deleted' % investor_id)
        # Status: Rejected
        #if investor.fk_status_id == HistoricalInvestor.STATUS_REJECTED:
        #    # Only Administrators are allowed to edit (recover) deleted investors
        #    if not self.request.user.has_perm('landmatrix.review_investor') and \
        #       not investor.history_user == self.request.user:
        #        raise Http404('Investor %s has been rejected' % investor_id)
        return investor

    def _get_public_investor(self):
        # TODO: Cache result for user
        return Investor.objects.filter(investor_identifier=self.kwargs.get('investor_id')).first()


class InvestorListView(TableGroupView):

    template_name = "grid/investors.html"
    doc_type = "investor"
    QUERY_LIMITED_GROUPS = ["all", ]
    DEFAULT_GROUP = "by-role"
    COLUMN_GROUPS = {
        "role": ["roles", ],
        "classification": ["classification_display", ],
        "fk_country": ["fk_country_display", ],
        "all": ["investor_identifier", "name", "fk_country_display", "classification_display", "top_investors",
                "deal_count"]
    }
    GROUP_COLUMNS_LIST = COLUMN_GROUPS["all"]
    GROUP_NAMES = {
        "fk_country": _("Country of registration/origin"),
    }
    COLUMN_LABELS_MAP = {
        'investor_identifier': _('ID'),
        'investor_count': _('Investors'),
        'deal_count': _('Deals'),
        'top_investors': _('Top investors'),
        'parent_companies': _('Parent companies'),
        'roles': _('Role'),
    }
    variable_table = get_investor_variable_table()
    ID_FIELD = 'investor_identifier'
    DEFAULT_ORDER_BY = ID_FIELD
    GROUP_COLUMNS = ('investor_count', )
    ORDER_MAP = {
        'investor_count': '_count',
    }

    def dispatch(self, request, *args, **kwargs):
        if not kwargs.get('group'):
            kwargs["group"] = "all"
        return super(InvestorListView, self).dispatch(request, *args, **kwargs)

    def add_status_logic(self, query):
        """
        Add status filter logic based upon user
        :param query:
        :return:
        """
        # collect a proper and authorized-for-that-user status list from the requet paramert
        request_status_list = self.request.GET.getlist('status', []) if self.request else []
        if request_status_list and (self.request.user.is_superuser or
                                    self.request.user.has_perm('landmatrix.review_investor')):
            status_list_get = [int(status) for status in request_status_list
                               if (status.isnumeric() and int(status) in dict(InvestorBase.STATUS_CHOICES).keys())]
            if status_list_get:
                self.status_list = status_list_get

        query['filter'].append({
            "terms": {"fk_status": self.status_list}
        })
        return query

    def add_public_logic(self, query):
        """
        Set public filter logic to none
        :param query:
        :return:
        """
        return query

    def get_investor_filter(self, investors):
        """
        Get investor filter
        :param investors:
        :return:
        """
        return Filter(variable='_id', operator='in', value=investors)

    def get_group_item(self, result):
        """
        Add aggregate columns to group items
        :param result:
        :return:
        """
        item = super().get_group_item(result)
        item['investor_count'] = [result['doc_count'], ]
        return item

    def clean_roles(self, value, result):
        if value:
            value['display'] = dict(InvestorBase.ROLE_CHOICES).get(value['value'])
            return value
        else:
            return value

    def get_field_label(self, column):
        return get_investor_field_label(column)


class DeleteInvestorView(InvestorUpdateView):
    
    success_message = _('The investor #{} has been marked for deletion. It will be reviewed and deleted soon.')
    success_message_admin = _('The investor #{} has been deleted successfully.')

    def get_object(self):
        # TODO: Cache result for user
        investor_id = self.kwargs.get('investor_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalInvestor.objects
        if not self.request.user.has_perm('landmatrix.review_investor'):
            queryset = queryset.public()
        try:
            if history_id:
                investor = queryset.get(id=history_id)
            else:
                investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Investor %s does not exist (%s)' % (investor_id, str(e)))
        if not self.request.user.has_perm('landmatrix.change_investor'):
            if investor.fk_status_id == investor.STATUS_DELETED:
                raise Http404('Investor %s has already been deleted' % investor_id)
        return investor

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        hinvestor = self.get_object()
        involvements = list(hinvestor.involvements.all())
        venture_involvements = list(hinvestor.venture_involvements.all())
        investor_involvements = list(hinvestor.investors.all())
        # Create new historical activity
        hinvestor.pk = None
        if self.request.user.has_perm('landmatrix.delete_investor'):
            hinvestor.fk_status_id = hinvestor.STATUS_DELETED
        else:
            hinvestor.fk_status_id = hinvestor.STATUS_TO_DELETE
        hinvestor.history_user = self.request.user
        hinvestor.history_date = datetime.now()
        hinvestor.public_version = None
        hinvestor.save()
        for involvement in involvements:
            involvement.pk = None
            involvement.fk_investor = hinvestor
            involvement.save()
        for involvement in venture_involvements:
            involvement.pk = None
            involvement.fk_venture = hinvestor
            involvement.save()
        for involvement in investor_involvements:
            involvement.pk = None
            involvement.fk_investor = hinvestor
            involvement.save()

        if self.request.user.has_perm('landmatrix.delete_investor'):
            hinvestor.update_public_investor()

        # Create success message
        if self.request.user.has_perm('landmatrix.delete_investor'):
            messages.success(self.request, self.success_message_admin.format(hinvestor.investor_identifier))
        else:
            #self.create_investor_changeset(hinvestor)
            messages.success(self.request, self.success_message.format(hinvestor.investor_identifier))

        return HttpResponseRedirect(reverse('investor_detail', kwargs={'investor_id': hinvestor.investor_identifier}))


class RecoverInvestorView(InvestorUpdateView):

    success_message = None
    success_message_admin = _('The investor #{} has been recovered successfully.')

    def get_object(self):
        # TODO: Cache result for user
        investor_id = self.kwargs.get('investor_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalInvestor.objects
        if not self.request.user.has_perm('landmatrix.review_investor'):
            queryset = queryset.public()
        try:
            if history_id:
                investor = queryset.get(id=history_id)
            else:
                investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Investor %s does not exist (%s)' % (investor_id, str(e)))
        if not self.request.user.has_perm('landmatrix.change_investor'):
            if investor.fk_status_id != investor.STATUS_DELETED:
                raise Http404('Investor %s is already active' % investor_id)
        return investor

    def get(self, request, *args, **kwargs):
        hinvestor = self.get_object()
        return HttpResponseRedirect(reverse('investor_detail', kwargs={'investor_id': hinvestor.investor_identifier}))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        hinvestor = self.get_object()
        involvements = list(hinvestor.involvements.all())
        venture_involvements = list(hinvestor.venture_involvements.all())
        investor_involvements = list(hinvestor.investors.all())
        if not self.request.user.has_perm('landmatrix.change_investor'):
            return HttpResponseRedirect(reverse('investor_detail', kwargs={'investor_id': hinvestor.investor_identifier}))
        # Create new historical activity
        hinvestor.pk = None
        hinvestor.fk_status_id = hinvestor.STATUS_OVERWRITTEN
        hinvestor.history_user = self.request.user
        hinvestor.history_date = datetime.now()
        hinvestor.save()
        for involvement in involvements:
            involvement.pk = None
            involvement.fk_investor = hinvestor
            involvement.save()
        for involvement in venture_involvements:
            involvement.pk = None
            involvement.fk_venture = hinvestor
            involvement.save()
        for involvement in investor_involvements:
            involvement.pk = None
            involvement.fk_investor = hinvestor
            involvement.save()
        hinvestor.update_public_investor()

        # Create success message
        messages.success(self.request, self.success_message_admin.format(hinvestor.investor_identifier))

        return HttpResponseRedirect(reverse('investor_detail', kwargs={'investor_id': hinvestor.investor_identifier}))
