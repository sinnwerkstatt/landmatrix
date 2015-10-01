import random

from django.views.generic import TemplateView
from landmatrix.models import *
from api.views import deals_json_view


# Create your views here.
class MapView(TemplateView): 
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        print('MapView.get_context_data()')
        context = super(MapView, self).get_context_data(**kwargs)
        deal_list = []

        location_attributes = sorted(ActivityAttributeGroup.objects.filter(attributes__icontains="point_lat")[:50], key=lambda x: random.random())

        r = requests.get('http://127.0.0.1/api/api/deals.json?limit=100')
        print('RESPONSE:', r)



        for location in location_attributes:
            intention_attributes = ActivityAttributeGroup.objects.filter(attributes__icontains="intention", fk_activity_id=location.fk_activity_id)
            deal = {
                "deal_id": location.fk_activity_id,
                "point_lat": location.attributes.get("point_lat"),
                "point_lon": location.attributes.get("point_lon"),
                "intention": intention_attributes and intention_attributes[0].attributes.get("intention") or "",
            }
            deal_list.append(deal)

        context['ActivityAttribute_list'] = deal_list
        #raise Exception(deal_list)

# To see ALL markers use EXCLUDE + take out Sorted, Random and [:N°]
            #exclude(attributes__icontains="°").\
            #exclude(attributes__icontains="04.738 N").\
            #exclude(attributes__icontains="-3.0001328124999426666666cro").\
            #exclude(attributes__icontains="4.134665")
        #print (context)
        #return None
        return context