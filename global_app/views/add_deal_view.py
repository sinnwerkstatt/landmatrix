from global_app.views.save_deal_view import SaveDealView, FORMS
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
            for name, Form in FORMS:
                new_form = Form() if not data else Form(data)
                forms.append(new_form)
            return forms
