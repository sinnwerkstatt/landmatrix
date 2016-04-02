from grid.views.save_deal_view import SaveDealView
from landmatrix.models.activity import Activity
from django.db.models import Max

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AddDealView(SaveDealView):

    template_name = 'add-deal.html'

    def get_activity(self, **kwargs):
        activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max'] + 1
        return Activity(activity_identifier=activity_identifier, fk_status_id=1)

    def get_forms(self, data=None):
            forms = []
            for form in self.FORMS:
                forms.append(form(data or None))
            return forms
