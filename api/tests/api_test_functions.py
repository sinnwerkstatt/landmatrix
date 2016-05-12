from django.db import connection
from django.db.utils import ProgrammingError

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
import json


class ApiTestFunctions(TestCase):

    PREFIX = '/api/'

    def url(self, resource): return self.PREFIX + resource + self.POSTFIX

    def url_id(self, resource, id): return self.PREFIX + resource + self.INFIX + str(id) + self.POSTFIX

    def get_content(self, resource):
        response = self.client.get(self.url(resource))
        self.assertEqual(200, response.status_code)
        try:
            return json.loads(response.content.decode('utf-8'))
        except ValueError as e:
            print(response.content.decode('utf-8'))
            raise e




