#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Populates the operational companies with country and classification'

    def handle(self, *args, **options):
        from landmatrix.models import InvestorActivityInvolvement

        iai = InvestorActivityInvolvement.objects.all()
        for involvement in iai:
            if involvement.fk_investor:
            	investor = involvement.fk_investor
            	investor.fk_country = involvement.fk_activity.target_country
            	investor.classification = '10'
            	investor.save()
