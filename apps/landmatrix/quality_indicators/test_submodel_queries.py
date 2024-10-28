import pytest
from django.db import connection, models
from django.db.models.expressions import OuterRef
from django.db.models.query_utils import Q

from .submodel_queries import _q_any, _q_all, _q_multiple


class Person(models.Model):
    """A simple person model for testing purposes only."""

    name = models.CharField(max_length=100)
    age = models.IntegerField()

    mentor = models.ForeignKey(
        "self",
        null=True,
        default=None,
        on_delete=models.CASCADE,
        related_name="pupils",
    )

    class Meta:
        app_label = "test_app"


ALI = Person(name="Ali", age=25)
JANNIS = Person(name="Jannis", age=22)
TJORVE = Person(name="Tjorve", age=29)

FUCHS = Person(name="Fuchs", age=9, mentor=ALI)
BRAN = Person(name="Bran", age=11, mentor=TJORVE)
BRAN2 = Person(name="Bran", age=14, mentor=TJORVE)

MENTORS = [ALI, JANNIS, TJORVE]
PUPILS = [FUCHS, BRAN, BRAN2]

PUPILS_SUBQUERY = Person.objects.filter(
    mentor=OuterRef("pk"),
).values("mentor")


@pytest.fixture()
def person_model(transactional_db):  # need transactional here for some reason
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Person)

    yield Person

    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(Person)


@pytest.mark.skip
def test_q_any(person_model):

    def q_any_pupils_younger_than(age: int) -> Q:
        return _q_any(PUPILS_SUBQUERY, Q(age__lt=age))

    person_model.objects.bulk_create(MENTORS)
    person_model.objects.bulk_create(PUPILS)

    assert list(
        person_model.objects.filter(q_any_pupils_younger_than(12)),
    ) == [ALI, TJORVE], "Any of Ali's and Tjorve's pupils is younger than 12."

    assert list(
        person_model.objects.filter(q_any_pupils_younger_than(10)),
    ) == [ALI], "Any of Ali's pupils is younger than 10."


@pytest.mark.skip
def test_q_all(person_model):

    def q_all_pupils_older_than(age: int) -> Q:
        return _q_all(PUPILS_SUBQUERY, Q(age__gt=age))

    person_model.objects.bulk_create(MENTORS)
    person_model.objects.bulk_create(PUPILS)

    assert list(
        person_model.objects.filter(q_all_pupils_older_than(8)),
    ) == [ALI, TJORVE], "All of Ali's and Tjorve's pupils are older than 8."

    assert list(
        person_model.objects.filter(q_all_pupils_older_than(10)),
    ) == [TJORVE], "All of Tjorve's pupils are older than 10."


@pytest.mark.skip
def test_q_multiple(person_model):

    def q_multiple_pupils_named(name: str) -> Q:
        return _q_multiple(PUPILS_SUBQUERY, Q(name=name))

    person_model.objects.bulk_create(MENTORS)
    person_model.objects.bulk_create(PUPILS)

    assert list(
        person_model.objects.filter(q_multiple_pupils_named("Bran")),
    ) == [TJORVE], "Tjorve has two pupils called Bran."
