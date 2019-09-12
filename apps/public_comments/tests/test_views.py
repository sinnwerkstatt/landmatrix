from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
from threadedcomments.models import ThreadedComment

from apps.grid.tests.views.base import PermissionsTestCaseMixin
from apps.landmatrix.models import Activity
from apps.public_comments.forms import PublicCommentForm


class EditCommentViewTestCase(PermissionsTestCaseMixin,
                              TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        super().setUp()

        user = get_user_model().objects.get(username='reporter')
        self.activity = Activity.objects.get(id=10)
        self.comment = ThreadedComment.objects.create(user=user,
                                                      comment='comment',
                                                      content_object=self.activity,
                                                      site_id=1)

    def test(self):
        data = MultiValueDict({
            'name': ['name'],
            'email': ['reporter@example.com'],
            'url': ['https://example.com'],
            'comment': ['new comment'],
            'g-recaptcha-response': ['g-recaptcha-response'],
            'next': ['/next'],
        })
        form = PublicCommentForm(self.activity)
        data.update(form.generate_security_data())
        self.client.login(username='superuser', password='test')
        response = self.client.post(reverse('comments-edit', kwargs={'comment_id': self.comment.id}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual('/next?c=10', response.url)
        self.assertEqual('new comment', ThreadedComment.objects.first().comment)
