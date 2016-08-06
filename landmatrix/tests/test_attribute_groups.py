__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils import timezone
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.language import Language
from landmatrix.tests.with_status import WithStatus

class TestAttributeGroups(WithStatus):

    def setUp(self):
        WithStatus.setUp(self)
        Activity(
            activity_identifier=1,
#                version=1,
                availability=0.5, fully_updated=timezone.now(),
            fk_status=self.status
        ).save()
        self.activity = Activity.objects.last()
        Language(english_name='English', local_name='English', locale='en').save()
        self.language = Language.objects.last()
        self.attributes = { 'blah': 'blub', 'yadda': 1.2345 }
        for key, value in self.attributes.items():
            ActivityAttribute.objects.create(
                fk_activity=self.activity,
                fk_language=self.language,
                name=key,
                value=value
            )

    def test_gets_created(self):
        group = ActivityAttribute(fk_activity=self.activity)
        self.assertEqual(self.activity.id, group.fk_activity.id)

    def test_gets_saved(self):
        group = ActivityAttribute(fk_activity=self.activity, fk_language=self.language)
        group.save()
        self.assertEqual(group, ActivityAttribute.objects.last())

    def test_string_contains_language(self):
        self.assertTrue(
            ''.join(str(Language.objects.last()).split()) in ''.join(str(ActivityAttribute.objects.last()).split())
        )

