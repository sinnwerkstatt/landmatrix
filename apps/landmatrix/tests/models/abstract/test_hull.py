from freezegun import freeze_time

from django.utils import timezone

from apps.landmatrix.tests.helpers import AbstractModelTestCase
from apps.landmatrix.models.abstract import BaseHull


class TestHullBase(AbstractModelTestCase):
    abstract_model = BaseHull

    @freeze_time("2024-07-26")
    def test_creation(self):
        hull: BaseHull = self.derived_model.objects.create()

        assert not hull.deleted
        assert hull.deleted_comment == ""

        assert hull.first_created_by is None
        assert (
            hull.first_created_at == timezone.now()
        ), "Initialized to UTC now on creation."

    def test_creation_with_date(self):
        hull: BaseHull = self.derived_model.objects.create(
            first_created_at="2012-07-26",
        )

        assert (
            hull.first_created_at == "2012-07-26"
        ), "Initialized to given datetime, i.e. 2012-07-26."
