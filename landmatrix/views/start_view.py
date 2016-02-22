__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.views.generic import TemplateView



class StartView(TemplateView):
    template_name = "start_mock.html"