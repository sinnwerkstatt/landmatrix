import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "apps/landmatrix/fixtures/countries_and_regions.json")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create(
            id=1, first_name="Land", last_name="Matrix", username="lama"
        )


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         d3 = Deal.objects.create(
#             id=3,
#             negotiation_status=[{"value": "Expression of interest"}]
#         )
