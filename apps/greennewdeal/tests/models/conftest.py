# import pytest
# from apps.landmatrix.models import HistoricalActivity
#
#
# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         h1 = HistoricalActivity(activity_identifier=1, fk_status_id=2)
#         h1.save(update_elasticsearch=False)
