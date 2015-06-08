__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils import timezone
from landmatrix.models import Involvement, Activity, PrimaryInvestor, Stakeholder
from landmatrix.tests.with_status import WithStatus


class TestInvolvement(WithStatus):

    DUMMY_INVESTMENT_RATIO = 1.23

    def setUp(self):
        WithStatus.setUp(self)
        Activity(
            activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now(),
            fk_status=self.status
        ).save()
        PrimaryInvestor(
            primary_investor_identifier=1, name='A Silly Name', version=2,
            fk_status=self.status
        ).save()
        Stakeholder(stakeholder_identifier=1, version=2, fk_status=self.status).save()


    def test_gets_created(self):
        involvement = Involvement()
        self.assertIsInstance(involvement, Involvement)

    def test_accepts_investment_ratio(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        self.assertEqual(self.DUMMY_INVESTMENT_RATIO, involvement.investment_ratio)

    def test_str(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        self.assertTrue(str(self.DUMMY_INVESTMENT_RATIO) in str(involvement))

    def test_save(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        old_count = Involvement.objects.count()
        involvement.save()
        self.assertEqual(old_count+1, Involvement.objects.count())
        self.assertEqual(
            self.DUMMY_INVESTMENT_RATIO,
            float(Involvement.objects.last().investment_ratio)
        )

    def test_create_with_activity(self):
        Involvement(
            investment_ratio=self.DUMMY_INVESTMENT_RATIO, fk_activity=Activity.objects.last()
        ).save()

        self.assertIsInstance(Involvement.objects.last().fk_activity, Activity)
        self.assertEqual(Activity.objects.last(), Involvement.objects.last().fk_activity)

    def test_create_with_all_referenced_objects(self):
        Involvement(
            investment_ratio=self.DUMMY_INVESTMENT_RATIO,
            fk_activity=Activity.objects.last(),
            fk_stakeholder=Stakeholder.objects.last(),
            fk_primary_investor=PrimaryInvestor.objects.last()
        ).save()

        self.assertEqual(Activity.objects.last(), Involvement.objects.last().fk_activity)
        self.assertEqual(Stakeholder.objects.last(), Involvement.objects.last().fk_stakeholder)
        self.assertEqual(PrimaryInvestor.objects.last(), Involvement.objects.last().fk_primary_investor)

    def test_string_with_referenced_objects(self):
        Involvement(
            investment_ratio=self.DUMMY_INVESTMENT_RATIO,
            fk_activity=Activity.objects.last(),
            fk_stakeholder=Stakeholder.objects.last(),
            fk_primary_investor=PrimaryInvestor.objects.last()
        ).save()

        # Need to strip all spaces when checking if Involvement string representation contains
        # string representation of the subobjects because the subobjects are indnented.
        self.assertTrue(
            str(Activity.objects.last()).replace(' ', '')
            in str(Involvement.objects.last()).replace(' ', '')
        )
        self.assertTrue(
            str(Stakeholder.objects.last()).replace(' ', '')
            in str(Involvement.objects.last()).replace(' ', '')
        )
        self.assertTrue(
            str(PrimaryInvestor.objects.last()).replace(' ', '')
            in str(Involvement.objects.last()).replace(' ', '')
        )
