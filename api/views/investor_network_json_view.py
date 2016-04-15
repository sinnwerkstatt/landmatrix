from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

from landmatrix.models.investor import Investor, InvestorVentureInvolvement

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

VERBOSE = True

class InvestorNetworkJSONView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        operational_stakeholder = Investor.objects.get(pk=int(request.GET.get('operational_stakeholder')))
        investordiagram = int(request.GET.get('operational_stakeholder_diagram'))
        involvements = InvestorVentureInvolvement.objects.filter(fk_venture=operational_stakeholder)
        if VERBOSE:
            print(operational_stakeholder)
            print(involvements)
        stakeholder_involvements = involvements.filter(role='ST')
        investor_involvements = involvements.filter(role='IN')

        nodes = []
        stakeholder_index = None
        if stakeholder_involvements.count():
            nodes.append({
                "name": "Stakeholders",
                "id": "stakeholders"
            })
            stakeholder_index = 0

        investor_index = None
        if investor_involvements.count():
            investor_index = len(nodes)
            nodes.append({
                "name": "Investors",
                "id": "investors"
            })

        stakeholder_start_index = len(nodes)
        for involvement in stakeholder_involvements:
            nodes.append({
                'name': involvement.fk_investor.name,
                'id': 'stakeholder_{}'.format(involvement.fk_investor_id)
            })
        investor_start_index = len(nodes)
        for involvement in investor_involvements:
            nodes.append({
                'name': involvement.fk_investor.name,
                'id': 'investor_{}'.format(involvement.fk_investor_id)
            })
        if VERBOSE:
            print(nodes)

        links = []

        for i, involvement in enumerate(stakeholder_involvements):
            links.append({
                'source': stakeholder_index,
                'target': stakeholder_start_index+i,
                'value': involvement.percentage
            })
        for i, involvement in enumerate(investor_involvements):
            links.append({
                'source': investor_index,
                'target': investor_start_index+i,
                'value': involvement.percentage
            })

        return HttpResponse(json.dumps({'index': investordiagram, 'nodes': nodes, 'links': links}))