from pprint import pprint
import json

from django.template import loader
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.country import Country
from grid.views.save_deal_view import SaveDealView




def render_to_response(template_name, context, context_instance):
    """ Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments."""
    # Some deprecated arguments were passed - use the legacy code path
    return HttpResponse(render_to_string(template_name, context, context_instance))


def render_to_string(template_name, context, context_instance):
    return loader.render_to_string(template_name, context, context_instance)

