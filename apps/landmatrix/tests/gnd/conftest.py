import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "apps/landmatrix/fixtures/countries_and_regions.json")


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         d3 = Deal.objects.create(
#             id=3,
#             negotiation_status=[{"value": "Expression of interest"}]
#         )
