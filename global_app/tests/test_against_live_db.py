__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase

""" Since the database used is the test database and not the live database,
    and it is quite complicated to recreate fixture data that represent real
    life data, this test is run via an external script that compares the
    results of the queries in the 'get the detail' views with previously
    saved data on the live db. if the live db has been changed, defined state
    of the DB can be restored with the landmatrix_reference_data.sql dump in
    the data/ subdirectory.
    OBVIOUSLY this should NOT be done on a live system, so if you want tests
    on the live system to pass, disable this test!
    TO DO: en-/disable it from settings file
"""
class TestAgainstLiveDB(TestCase):

    def test_compare_to_v1_data(self):
        import os
        from subprocess import call
        dir = os.path.dirname(os.path.realpath(__file__))
        num_errors = call(['python', dir+'/compare_sql_results.py'])
        self.assertEqual(0, num_errors)
