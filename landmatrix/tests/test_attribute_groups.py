__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils import timezone
from landmatrix.models import ActivityAttributeGroup, StakeholderAttributeGroup, \
    Activity, Stakeholder, Language
from landmatrix.tests.with_status import WithStatus

class TestAttributeGroups(WithStatus):

    def setUp(self):
        WithStatus.setUp(self)
        Activity(
            activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now(),
            fk_status=self.status
        ).save()
        self.activity = Activity.objects.last()
        Stakeholder(stakeholder_identifier=1, version=2, fk_status=self.status).save()
        self.stakeholder = Stakeholder.objects.last()
        Language(english_name='English', local_name='English', locale='en').save()
        self.language = Language.objects.last()
        self.attributes = { 'blah': 'blub', 'yadda': 1.2345 }
        ActivityAttributeGroup(
            fk_activity=self.activity, fk_language=self.language,
            attributes=self.attributes
        ).save()

    def test_gets_created(self):
        group = ActivityAttributeGroup(fk_activity=self.activity)
        self.assertEqual(self.activity.id, group.fk_activity.id)
        group2 = StakeholderAttributeGroup(fk_stakeholder=self.stakeholder)
        self.assertEqual(self.stakeholder.id, group2.fk_stakeholder.id)

    def test_gets_saved(self):
        group = ActivityAttributeGroup(fk_activity=self.activity, fk_language=self.language)
        group.save()
        self.assertEqual(group, ActivityAttributeGroup.objects.last())

    def test_access_hstore_dictfield(self):
        group = ActivityAttributeGroup.objects.last()
        self.assertEqual('blub', group.attributes['blah'])
        self.assertEqual(1.2345, float(group.attributes['yadda']))

    def test_string_contains_language(self):
        self.assertTrue(
            str(Language.objects.last()).replace(' ', '')
            in str(ActivityAttributeGroup.objects.last()).replace(' ', '')
        )

    def test_string_contains_attributes(self):
        for k in self.attributes:
            self.assertTrue(
                str(k) in str(ActivityAttributeGroup.objects.last())
            )

