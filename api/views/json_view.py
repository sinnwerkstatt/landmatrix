from api.views.deals_json_view import DealsJSONView
from api.views.transnational_deals_json_view import TransnationalDealsJSONView
from api.views.implementation_status_json_view import ImplementationStatusJSONView
from api.views.intention_of_investment_json_view import IntentionOfInvestmentJSONView
from api.views.negotiation_status_json_view import NegotiationStatusJSONView

from django.views.generic.base import TemplateView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'




class JSONView(TemplateView):

    template_name = 'plugins/overview.html'

    targets = {
        'negotiation_status.json':             NegotiationStatusJSONView,
        'implementation_status.json':          ImplementationStatusJSONView,
        'intention_of_investment.json':        IntentionOfInvestmentJSONView,
        'transnational_deals.json':            TransnationalDealsJSONView,
        'deals.json':                          DealsJSONView,
    }
