
# Create your views here.
from django.template.context import RequestContext

from django.views.generic import TemplateView

from global_app.views.view_aux_functions import render_to_response

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class EditorView(TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        context = {'user': None}
        print('user:', request.user)
        if request.user.is_authenticated():
            context['user'] = request.user

        return render_to_response(self.template_name, context, RequestContext(request))
