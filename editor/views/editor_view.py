from django.shortcuts import redirect
from django.template.context import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from global_app.views.view_aux_functions import render_to_response

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class EditorView(TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.render_authenticated_user(request)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def render_authenticated_user(self, request):
        context = {
            'user': request.user,
            'latest_modified': self.latest_modified(),
            'latest_added': self.latest_added(),
            'latest_deleted': self.latest_deleted(),
            'attention_needed': self.attention_needed(request.user),
            'feedback_requests': self.feedback_requests(request.user)
        }
        return render_to_response(self.template_name, context, RequestContext(request))

    def latest_modified(self):
        
        return []

    def latest_added(self):
        return []

    def latest_deleted(self):
        return []

    def attention_needed(self, user):
        return []

    def feedback_requests(self, user):
        return []

