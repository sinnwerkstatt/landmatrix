from datetime import datetime

from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from grid.views.save_deal_view import SaveDealView
from landmatrix.models.activity import HistoricalActivity
from django.contrib import messages

class DeleteDealView(SaveDealView):
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

        if self.request.user.has_perm('landmatrix.delete_activity'):
            hactivity.update_public_activity()

        # Create success message
        if self.request.user.has_perm('landmatrix.delete_activity'):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
        else:
            self.create_activity_changeset(hactivity)
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier})) 


class RecoverDealView(SaveDealView):
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
        if not self.request.user.has_perm('landmatrix.delete_activity'):
            return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier})) 
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
        hactivity.update_public_activity()

        # Create success message
        messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))

        return HttpResponseRedirect(reverse('deal_detail', kwargs={'deal_id': hactivity.activity_identifier})) 