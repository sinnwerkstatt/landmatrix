__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.views.generic import TemplateView
from django.template import RequestContext

class MapView(TemplateView):
    template_name = 'map/map.html'