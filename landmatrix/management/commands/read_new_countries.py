from pprint import pprint

from django.core.management.base import BaseCommand

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.country import Country

import csv

from landmatrix.models.investor import Investor



class Command(BaseCommand):

    renamed_countries = {

    }
    def add_arguments(self, parser):
        parser.add_argument(
            '--show_dropped_countries', action='store_true', dest='show_dropped_countries', default=False
        )
        parser.add_argument(
            '--show_additional_countries', action='store_true', dest='show_additional_countries', default=False
        )
        parser.add_argument(
            '--show_orphaned_deals', action='store_true', dest='show_orphaned_deals', default=False
        )
        parser.add_argument(
            '--set_target_country_flags', action='store_true', dest='set_target_country_flags', default=False
        )

    def handle(self, *args, **options):
        if options['show_dropped_countries']:
            self.show_dropped_countries()
        elif options['show_additional_countries']:
            self.show_additional_countries()
        elif options['show_orphaned_deals']:
            self.show_orphaned_deals()
        elif options['set_target_country_flags']:
            self.set_target_country_flags()
        else:
            print(options)

    def show_dropped_countries(self):
        dropped_countries = get_old_countries() - get_new_countries()
        pprint(sorted(dropped_countries), compact=True)

    def show_additional_countries(self):
        additional_countries = get_new_countries() - get_old_countries()
        pprint(sorted(additional_countries), compact=True)

    def show_orphaned_deals(self):
        orphaned_countries = get_orphaned_countries()
        for country in set(orphaned_countries):
            print(country.name)
            pprint(
                sorted(
                    [
                        (deal.activity_identifier, get_investor_country(deal))
                        for deal in deals_in_country(country)
                    ]
                )
            )

    def set_target_country_flags(self):
        country_ids = ActivityAttribute.objects.filter(name='target_country')
        countries = Country.objects.filter(pk__in=[aa.value for aa in country_ids])
        for country in countries:
            country.is_target_country = True
            country.save()


def get_investor_country(deal):
    investors = Investor.objects.filter(investoractivityinvolvement__fk_activity=deal)
    countries = [Country.objects.get(pk=country).name for country in set(investors.values_list('fk_country', flat=True))]
    return countries

def get_orphaned_countries():
    dropped_countries = get_old_countries() - get_new_countries()
    dropped_countries_ids = list(Country.objects.filter(name__in=dropped_countries).values_list('id', flat=True))
    deals_in_dropped_countries = ActivityAttribute.objects.filter(name='target_country')
    return [
        Country.objects.get(pk=aa.value) for aa in deals_in_dropped_countries
    ]


def get_new_countries():
    new_countries = set()
    with open('target_countries_regions.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)    # skip header line
        for row in reader:
            country, region = row
            new_countries.add(country)
    return new_countries


def get_old_countries():
    return set(country.name for country in Country.objects.all())


def deals_in_country(country):
    return set(Activity.objects.filter(attributes__name='target_country', attributes__value=country.id))