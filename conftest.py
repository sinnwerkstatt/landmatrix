from pathlib import Path

import pytest

from django.core.management import call_command

ROOT_DIR = Path(__file__).parent
FIXTURES_DIR = ROOT_DIR / "apps/landmatrix/fixtures"


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            FIXTURES_DIR / "countries_and_regions.json",
        )
        call_command(
            "loaddata",
            FIXTURES_DIR / "users_and_groups.json",
        )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
