from django.core.management.base import BaseCommand
from django.db import connection

from apps.landmatrix.models.investor import InvestorVentureInvolvement
from apps.landmatrix.models.new import Involvement


class Command(BaseCommand):
    def handle(self, *args, **options):
        for inv_old in InvestorVentureInvolvement.objects.all():
            inv_old: InvestorVentureInvolvement
            Involvement.objects.create(
                id=inv_old.id,
                parent_investor_id=inv_old.investor_id,
                child_investor_id=inv_old.venture_id,
                role=inv_old.role,
                investment_type=inv_old.investment_type or [],
                percentage=inv_old.percentage,
                loans_amount=inv_old.loans_amount,
                loans_currency=inv_old.loans_currency,
                loans_date=inv_old.loans_date,
                parent_relation=inv_old.parent_relation,
                comment=inv_old.comment,
            )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval('landmatrix_involvement_id_seq', (SELECT MAX(id) from landmatrix_involvement))"
            )
