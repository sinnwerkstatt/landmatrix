from django.test import TestCase

from apps.grid.forms.deal_action_comment_form import DealActionCommentForm
from apps.landmatrix.models import HistoricalActivity


class GridDealActionCommentFormTestCase(TestCase):

    fixtures = [
        'status'
    ]

    def setUp(self):
        self.form =  DealActionCommentForm()
        self.form.data = {'tg_action_comment': 'test'}

    def test_get_attributes(self):
        attributes = self.form.get_attributes()
        self.assertEqual({}, attributes)

    def test_get_data(self):
        activity = HistoricalActivity.objects.create(id=1, activity_identifier=1, comment='action comment')
        activity.attributes.create(name='tg_action_comment', value='test')
        data = self.form.get_data(activity)
        self.assertEqual(['action comment'], data.getlist('tg_action_comment'))
