from grid.views.save_deal_view import SaveDealView
from landmatrix.models.activity import Activity
from django.db.models import Max

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AddDealView(SaveDealView):
    template_name = 'add-deal.html'
    #success_message = _('Added successfully.')

    def post(self, request, *args, **kwargs):
    	# Create activity first
        activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max'] + 1
        self.activity = Activity.objects.create(
        	activity_identifier=activity_identifier,
        	fk_status_id=1
        )
        return super(AddDealView, self).post(request, *args, **kwargs)

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            prefix = self.get_form_prefix(form_class)
            form = form_class(data=data, files=files, prefix=prefix)
            forms.append(form)

        return forms
