from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import transaction
from django.db.models import Max
from django.forms import BaseFormSet
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from grid.forms.country_specific_forms import get_country_specific_form_classes
from grid.forms.deal_action_comment_form import DealActionCommentForm
from grid.forms.deal_data_source_form import DealDataSourceForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.utils import has_perm_approve_reject
from grid.views.base import TableGroupView
from grid.views.utils import PUBLIC_FORMS, USER_FORMS, DEAL_FORMS
from landmatrix.models import HistoricalActivity, Activity, Country, DealHistoryItem, ActivityAttributeGroup, \
    HistoricalActivityAttribute, HistoricalInvestorActivityInvolvement, ActivityFeedback, ActivityChangeset
from landmatrix.pdfgen import PDFViewMixin


class DealListView(TableGroupView):

    template_name = "grid/deals.html"

    def dispatch(self, request, *args, **kwargs):
        if not kwargs.get("group"):
            kwargs["group"] = "all"
        return super(DealListView, self).dispatch(request, *args, **kwargs)

    def _get_group_agg(self, group):
        return {
            self.group: {
                'terms': {
                    'field': group,
                    'size': 10000,
                    'order': self.order_by,
                },
                'aggs': {
                    'deal_size_sum': {
                        'sum': {
                            'field': 'deal_size'
                        }
                    },
                    'availability_avg': {
                        'avg': {
                            'field': 'availability'
                        }
                    },
                    'all': {
                        'terms': {
                            'field': self.AGGREGATE_COLUMNS.get(group, group)
                        }
                    },
                }
            }
        }

    def get_group_item(self, result):
        """
        Add aggregate columns to group items
        :param result:
        :return:
        """
        item = super().get_group_item(result)
        item['deal_count'] = [result['doc_count'], ]
        item['deal_size'] = [int(result['deal_size_sum']['value']), ]
        item['availability'] = [result['availability_avg']['value'], ]
        return item


class DealBaseView(TemplateView):

    FORMS = DEAL_FORMS
    deal_id = None
    success_message = _('Your changes to the deal have been submitted successfully. The changes will be reviewed and published soon.')
    success_message_admin = _('Your changes to the deal have been saved successfully.')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        if self.request.method != 'POST':
            context['forms'] = self.get_forms()
        context['kwargs'] = self.kwargs
        return context

    def get_forms(self, data=None, files=None):
        raise NotImplementedError("get_forms must be implemented in "
                                  "subclasses.")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        forms = self.get_forms(
            data=self.request.POST, files=self.request.FILES)
        if all(form.is_valid() for form in forms):
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

    def form_valid(self, forms):
        old_hactivity = self.get_object()
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        is_admin = self.request.user.has_perm('landmatrix.change_activity')
        is_editor = self.request.user.has_perm('landmatrix.review_activity')

        if old_hactivity.fk_status_id == HistoricalActivity.STATUS_PENDING:
            # Only editors and administrators are allowed to edit pending versions
            if not is_editor and not is_admin:
                return HttpResponseForbidden('Deal version is pending')

        # Don't create new version if rejected
        if 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, old_hactivity):
            hactivity = old_hactivity
        else:
            # Create new historical activity
            hactivity = HistoricalActivity(
                activity_identifier=old_hactivity.activity_identifier,
                fk_status_id=HistoricalActivity.STATUS_PENDING,
                history_user=self.request.user)
            hactivity.save(update_elasticsearch=False)

            # Create new activity attributes
            hactivity.comment = self.create_attributes(hactivity, forms)
            form = self.get_form_by_type(forms, DealActionCommentForm)
            if form:
                hactivity.fully_updated = self.get_fully_updated(form)
            else:
                hactivity.fully_updated = False
            hactivity.save(update_elasticsearch=False)
            self.create_involvement(hactivity, investor_form)

            if not is_admin:
                self.create_activity_changeset(hactivity)

        # Create activity feedback
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            self.create_activity_feedback(hactivity, form)

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
            hactivity.approve_change(self.request.user, hactivity.comment)
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            hactivity.reject_change(self.request.user, hactivity.comment)
        else:
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        return redirect('deal_detail', deal_id=hactivity.activity_identifier)

    def form_invalid(self, forms):
        messages.error(self.request, _('Please correct the error below.'))

        context = self.get_context_data(**self.kwargs)
        context['forms'] = forms
        return self.render_to_response(context)

    def create_attributes(self, activity, forms):
        action_comment = ''
        # Create new attributes
        for form in forms:
            if form.Meta.name in ('action_comment', 'user_information'):
                action_comment = form.cleaned_data['tg_action_comment']

            attributes = form.get_attributes(request=self.request)
            if not attributes:
                continue
            # Formset?
            if isinstance(attributes, list):
                # Loop forms
                for count, form_attributes in enumerate(attributes):
                    if form_attributes:
                        aag, created = ActivityAttributeGroup.objects.get_or_create(
                            name='%s_%02i' % (form.Meta.name, count + 1), # two digits required for ordering
                        )
                        # Loop fields
                        for name, attribute in form_attributes.items():
                            if isinstance(attribute, dict):
                                attribute = [attribute]
                            # Loop values (= attributes)
                            for kwargs in attribute:
                                kwargs.update({
                                    'name': name,
                                    'fk_activity': activity,
                                    'fk_group': aag,
                                    'fk_language_id': 1,
                                })
                                aa = HistoricalActivityAttribute.objects.create(**kwargs)
            # Form
            elif attributes:
                aag, created = ActivityAttributeGroup.objects.get_or_create(
                    name=form.Meta.name
                )
                # Loop fields
                for name, attribute in attributes.items():
                    if not isinstance(attribute, (list, tuple)):
                        attribute = [attribute]
                    # Loop values (= attributes)
                    for kwargs in attribute:
                        kwargs.update({
                            'name': name,
                            'fk_activity': activity,
                            'fk_group': aag,
                            'fk_language_id': 1,
                        })
                        aa = HistoricalActivityAttribute.objects.create(**kwargs)

        return action_comment

    def create_involvement(self, hactivity, form):
        hinvestor = form.cleaned_data['operational_stakeholder']
        # Operating company given?
        if hinvestor:
            hinvolvement = HistoricalInvestorActivityInvolvement.objects.create(
                fk_activity=hactivity,
                fk_investor=hinvestor,
                fk_status_id=hactivity.STATUS_PENDING,
            )

    def get_form_by_type(self, forms, type):
        form = list(filter(lambda f: isinstance(f, type), forms))
        if len(form) == 0:
            return
        else:
            return form[0]

    def create_activity_feedback(self, activity, form):
        data = form.cleaned_data
        if data.get('assign_to_user', None):
            ActivityFeedback.objects.filter(fk_activity__activity_identifier=activity.activity_identifier).delete()
            feedback = ActivityFeedback.objects.create(
                fk_activity_id=activity.id,
                fk_user_assigned=data.get('assign_to_user'),
                fk_user_created=self.request.user,
                comment=data.get('tg_feedback_comment'),
            )

    def get_fully_updated(self, form):
        return form.cleaned_data.get('fully_updated', False)

    def create_activity_changeset(self, activity):
        # Create changeset (for review)
        country = activity.target_country
        try:
            user = self.request.user.userregionalinfo.super_user
        except (AttributeError, ObjectDoesNotExist):
            user = None
        changeset = ActivityChangeset.objects.create(
            fk_activity=activity,
            fk_country=country,
            #fk_region=country and country.region
            fk_user=user,
        )
        return changeset


class DealUpdateView(DealBaseView):

    FORMS = DEAL_FORMS

    template_name = 'grid/deal_form_update.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        activity = self.get_object()
        if not activity.is_editable(request.user):
            # Redirect to deal detail
            args = {'deal_id': activity.activity_identifier}
            if 'history_id' in kwargs:
                args['history_id'] = kwargs['history_id']
            return HttpResponseRedirect(reverse('deal_detail', kwargs=args))
        return super(DealUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, deal_id, history_id=None):
        context = super().get_context_data(**self.kwargs)
        context.update({
            'deal_id': deal_id,
            'history_id': history_id,
            'activity': self.get_object(),
            'export_formats': ("XML", "CSV", "XLS", "PDF"),
        })
        return context

    def get_object(self):
        # TODO: Cache result for user
        deal_id = self.kwargs.get('deal_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalActivity.objects
        try:
            if history_id:
                activity = queryset.get(id=history_id)
            else:
                #queryset = queryset.filter(fk_status_id__in=(HistoricalActivity.STATUS_ACTIVE,
                #                                             HistoricalActivity.STATUS_OVERWRITTEN,
                #                                             HistoricalActivity.STATUS_DELETED))
                activity = queryset.filter(activity_identifier=deal_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (deal_id, str(e)))
        # Status: Deleted
        #if activity.fk_status_id == HistoricalActivity.STATUS_DELETED:
        #    # Only Administrators are allowed to edit (recover) deleted deals
        #    if not self.request.user.has_perm('landmatrix.change_activity'):
        #        raise Http404('Activity %s has been deleted' % deal_id)
        # Status: Rejected
        #if activity.fk_status_id == HistoricalActivity.STATUS_REJECTED:
        #    # Only Administrators are allowed to edit (recover) deleted deals
        #    if not self.request.user.has_perm('landmatrix.review_activity') and \
        #       not activity.history_user == self.request.user:
        #        raise Http404('Activity %s has been rejected' % deal_id)
        return activity

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            forms.append(self.get_form(form_class, data=data, files=files))
        # Add country specific forms
        for form_class in get_country_specific_form_classes(self.get_object()):
            forms.append(self.get_form(form_class, data=data, files=files))
        return forms

    def get_form(self, form_class, data=None, files=None):
        prefix = issubclass(form_class, BaseFormSet) and form_class.Meta.name or None
        initial = form_class.get_data(self.get_object())
        if form_class == DealActionCommentForm:
            if 'tg_action_comment' in initial:
                del initial['tg_action_comment']
            if 'fully_updated' in initial:
                del initial['fully_updated']
        return form_class(initial=initial, files=files, data=data, prefix=prefix)

    #def render_to_response(self, *args, **kwargs):
    #    '''
    #    If we have a shapefile upload, just reload the page so it displays
    #    correctly
    #    '''
    #    # TODO: remove this hack, make the different area fields handle this
    #    if any(['_area' in key for key in self.request.FILES.keys()]):
    #        return HttpResponseRedirect(
    #            self.request.META.get('HTTP_REFERER', '/'))
    #    return super().render_to_response(*args, **kwargs)


class DealDetailView(PDFViewMixin, TemplateView):

    template_name = 'grid/deal_detail.html'
    pdf_export_url = 'deal_detail_pdf'
    pdf_render_url = 'deal_detail'

    def get_pdf_filename(self, request, *args, **kwargs):
        return 'deal_{deal_id}.pdf'.format(**kwargs)

    def get_object(self):
        # TODO: Cache result for user
        deal_id = self.kwargs.get('deal_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalActivity.objects
        if not self.request.user.is_authenticated:
            a = self._get_public_activity()
            if not a or not a.is_public:
                raise Http404('Activity %s is not public' % deal_id)
            queryset = queryset.public_or_deleted(self.request.user)
        try:
            if history_id:
                activity = queryset.get(id=history_id)
            else:
                activity = queryset.filter(activity_identifier=deal_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (deal_id, str(e)))
        # Status: Deleted
        if activity.fk_status_id == HistoricalActivity.STATUS_DELETED:
            # Only Administrators are allowed to edit (recover) deleted deals
            if not self.request.user.has_perm('landmatrix.change_activity'):
                raise Http404('Activity %s has been deleted' % deal_id)
        # Status: Rejected
        #if activity.fk_status_id == HistoricalActivity.STATUS_REJECTED:
        #    # Only Administrators are allowed to edit (recover) deleted deals
        #    if not self.request.user.has_perm('landmatrix.review_activity') and \
        #       not activity.history_user == self.request.user:
        #        raise Http404('Activity %s has been rejected' % deal_id)
        return activity

    def _get_public_activity(self):
        # TODO: Cache result for user
        return Activity.objects.filter(activity_identifier=self.kwargs.get('deal_id')).first()

    def get_context_data(self, deal_id, history_id=None):
        context = super(DealDetailView, self).get_context_data()
        activity = self.get_object()
        context['activity'] = activity
        context['public_activity'] = self._get_public_activity()
        context['forms'] = get_forms(activity, user=self.request.user)
        context['investor'] = activity.stakeholders
        context['history_id'] = history_id

        context['export_formats'] = ("XML", "CSV", "XLS", "PDF")

        return context

    def render_forms(self, request, context):
        return self.render_to_response(context=context)

    def render_forms_to_string(self, request, context):
        return render_to_string(template_name=self.template_name,
                                context=context,
                                request=request)


def display_valid_forms(forms):
    activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))[
                              'activity_identifier__max'] + 1
    activity = Activity(activity_identifier=activity_identifier, fk_status_id=1, version=1)
    for form in forms:
        if form.Meta.name == 'investor_info':
            print('investor_info', form.cleaned_data)
        elif form.Meta.name == 'data_source':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['type'] and isinstance(sub_form_data['type'], int):
                    field = DealDataSourceForm().fields['type']
                    choices = dict(field.choices)
                    sub_form_data['type'] = str(choices[sub_form_data['type']])
                group = create_attribute_group(activity, sub_form_data)
                print(form.Meta.name, group)
        elif form.Meta.name == 'location':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
                    sub_form_data['target_country'] = sub_form_data['target_country'].pk
                group = create_attribute_group(activity, sub_form_data)
                print(form.Meta.name, group)
        else:
            if any(form.cleaned_data.values()):
                group = create_attribute_group(activity, form.cleaned_data)
                print(form.Meta.name, group)
            else:
                print('no data sent:', form.Meta.name)


def display_invalid_forms(forms):
    for form in forms:
        if form.is_valid():
            print(form.__class__.__name__, form.cleaned_data)
        else:
            print(form.__class__.__name__, 'INVALID:', form.errors)


def get_forms(activity, user, prefix=None):
    forms = [get_form(activity, form, prefix) for form in PUBLIC_FORMS]
    if user.is_authenticated:
        forms.extend([get_form(activity, form, prefix) for form in USER_FORMS])
    if activity:
        for form_class in get_country_specific_form_classes(activity):
            form_tuple = (form_class.Meta.name, form_class)
            country_specific_form = get_form(activity, form_tuple)
            forms.append(country_specific_form)
    return forms


def get_form(activity, form_class, prefix=None):
    if hasattr(form_class[1], 'prefix') and form_class[1].prefix:
        prefix = prefix + form_class[1].prefix
    data = form_class[1].get_data(activity, prefix=prefix)
    return form_class[1](initial=data, prefix=prefix)


def deal_from_activity_id_and_timestamp(id_and_timestamp):
    from datetime import datetime
    from dateutil.tz import tzlocal
    if '_' in id_and_timestamp:
        activity_identifier, timestamp = id_and_timestamp.split('_')

        activity = Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()
        if activity is None:
            raise ObjectDoesNotExist('activity_identifier %s' % activity_identifier)

        history = activity.history.filter(history_date__lte=datetime.fromtimestamp(float(timestamp), tz=tzlocal())).\
            filter(fk_status_id__in=(2, 3)).last()
        if history is None:
            raise ObjectDoesNotExist('Public deal with activity_identifier %s as of timestamp %s' % (activity_identifier, timestamp))

        return DealHistoryItem.from_activity_with_date(history, datetime.fromtimestamp(float(timestamp), tz=tzlocal()))

    raise RuntimeError('should contain _ separating activity id and timestamp: ' + id_and_timestamp)


class DeleteDealView(DealBaseView):

    success_message = _('The deal #{} has been marked for deletion. It will be reviewed and deleted soon.')
    success_message_admin = _('The deal #{} has been deleted successfully.')

    def get_object(self):
        # TODO: Cache result for user
        deal_id = self.kwargs.get('deal_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalActivity.objects
        if not self.request.user.has_perm('landmatrix.review_activity'):
            queryset = queryset.public()
        try:
            if history_id:
                activity = queryset.get(id=history_id)
            else:
                activity = queryset.filter(activity_identifier=deal_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (deal_id, str(e)))
        if not self.request.user.has_perm('landmatrix.change_activity'):
            if activity.fk_status_id == activity.STATUS_DELETED:
                raise Http404('Activity %s has already been deleted' % deal_id)
        return activity

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        hactivity = self.get_object()
        involvements = list(hactivity.involvements.all())
        attributes = hactivity.attributes.all()
        # Create new historical activity
        hactivity.pk = None
        if self.request.user.has_perm('landmatrix.delete_activity'):
            hactivity.fk_status_id = hactivity.STATUS_DELETED
        else:
            hactivity.fk_status_id = hactivity.STATUS_TO_DELETE
        hactivity.history_user = self.request.user
        hactivity.history_date = datetime.now()
        hactivity.public_version = None
        hactivity.save()
        for hattribute in attributes:
            hattribute.pk = None
            hattribute.fk_activity_id = hactivity.id
            hattribute.save()
        for involvement in involvements:
            involvement.pk = None
            involvement.fk_activity = hactivity
            involvement.save()

        if self.request.user.has_perm('landmatrix.delete_activity'):
            hactivity.update_public_activity()

        # Create success message
        if self.request.user.has_perm('landmatrix.delete_activity'):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
        else:
            self.create_activity_changeset(hactivity)
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier}))


class DealRecoverView(DealBaseView):

    success_message = None
    success_message_admin = _('The deal #{} has been recovered successfully.')

    def get_object(self):
        # TODO: Cache result for user
        deal_id = self.kwargs.get('deal_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalActivity.objects
        if not self.request.user.has_perm('landmatrix.review_activity'):
            queryset = queryset.public()
        try:
            if history_id:
                activity = queryset.get(id=history_id)
            else:
                activity = queryset.filter(activity_identifier=deal_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (deal_id, str(e)))
        if not self.request.user.has_perm('landmatrix.change_activity'):
            if activity.fk_status_id != activity.STATUS_DELETED:
                raise Http404('Activity %s is already active' % deal_id)
        return activity

    def get(self, request, *args, **kwargs):
        hactivity = self.get_object()
        return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier}))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        hactivity = self.get_object()
        if not self.request.user.has_perm('landmatrix.change_activity'):
            return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier}))
        involvements = list(hactivity.involvements.all())
        attributes = hactivity.attributes.all()
        # Create new historical activity
        hactivity.pk = None
        hactivity.fk_status_id = hactivity.STATUS_OVERWRITTEN
        hactivity.history_user = self.request.user
        hactivity.history_date = datetime.now()
        hactivity.save()
        for hattribute in attributes:
            hattribute.pk = None
            hattribute.fk_activity_id = hactivity.id
            hattribute.save()
        for involvement in involvements:
            involvement.pk = None
            involvement.fk_activity = hactivity
            involvement.save()
        hactivity.update_public_activity()

        # Create success message
        messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))

        return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier}))


class DealCreateView(DealBaseView):

    template_name = 'grid/deal_form_add.html'
    success_message = _('The deal has been submitted successfully (#{}). It will be reviewed and published soon.')
    success_message_admin = _('The deal has been added successfully (#{}).')

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            prefix = issubclass(form_class, BaseFormSet) and form_class.Meta.name or None
            forms.append(form_class(data=data, files=files, prefix=prefix))
        return forms

    def form_valid(self, forms):
        activity_identifier = HistoricalActivity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max'] or 0
        activity_identifier += 1
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        # Create new historical activity
        hactivity = HistoricalActivity(
            activity_identifier=activity_identifier,
            history_user=self.request.user,
        )
        is_admin = self.request.user.has_perm('landmatrix.add_activity')
        hactivity.fk_status_id = hactivity.STATUS_PENDING
        hactivity.save()

        # Create new activity attributes
        hactivity.comment = self.create_attributes(hactivity, forms)
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            hactivity.fully_updated = self.get_fully_updated(form)
        else:
            hactivity.fully_updated = False
        hactivity.save(update_elasticsearch=False)
        self.create_involvement(hactivity, investor_form)

        # Create activity feedback
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            self.create_activity_feedback(hactivity, form)

        if is_admin:
            redirect_url = reverse(
                'deal_detail', kwargs={'deal_id': hactivity.activity_identifier})
        else:
            # TODO: check that is is correct, but all deals seems like a
            # reasonable place to redirect to, as these users can't see the
            # deal yet
            redirect_url = reverse('data')

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
            hactivity.approve_change(self.request.user, hactivity.comment)
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            hactivity.reject_change(self.request.user, hactivity.comment)
        else:
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        return HttpResponseRedirect(redirect_url)
