import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "apps/landmatrix/fixtures/countries_and_regions.json")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for gname in ["Reporters", "Editors", "Administrators"]:
            Group.objects.get_or_create(name=gname)

        u_rep, _ = User.objects.get_or_create(
            first_name="Land", last_name="Reporter", username="land_reporter"
        )
        if not u_rep.groups.filter(name="Reporters"):
            u_rep.groups.add(Group.objects.get(name="Reporters"))

        u_rep2, _ = User.objects.get_or_create(
            first_name="Land", last_name="Reporter2", username="land_reporter2"
        )
        if not u_rep2.groups.filter(name="Reporters"):
            u_rep2.groups.add(Group.objects.get(name="Reporters"))

        u_edit, _ = User.objects.get_or_create(
            first_name="Land", last_name="Editor", username="land_editor"
        )
        if not u_edit.groups.filter(name="Editors"):
            u_edit.groups.add(Group.objects.get(name="Editors"))

        u_adm, _ = User.objects.get_or_create(
            first_name="Land", last_name="Admin", username="land_admin"
        )
        if not u_adm.groups.filter(name="Administrators"):
            u_adm.groups.add(Group.objects.get(name="Administrators"))


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         d3 = Deal.objects.create(
#             id=3,
#             negotiation_status=[{"value": "Expression of interest"}]
#         )
