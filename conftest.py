import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "apps/landmatrix/fixtures/countries_and_regions.json")
        call_command("loaddata", "apps/landmatrix/fixtures/status.json")
        call_command("loaddata", "apps/landmatrix/fixtures/languages.json")
