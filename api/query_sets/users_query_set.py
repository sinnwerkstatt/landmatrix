from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from django.contrib.auth.models import User

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class UsersQuerySet(SimpleFakeQuerySet):
    def all(self):
        #if self.get_data.get('region'): #FIXME: Doesn't work, get_data returns request
        #    countries = Country.objects.filter(fk_region__slug=self.get_data['region']).order_by('name')
        #else:
        users = User.objects.all().order_by('first_name')
        return [[user.id, user.username, user.get_full_name()] for user in users]
