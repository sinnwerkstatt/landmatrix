from django_elasticsearch import Document, fields
from django_elasticsearch.registries import registry

from apps.greennewdeal.models import Investor, InvestorVentureInvolvement


# noinspection PyMethodMayBeStatic
@registry.register_document
class InvestorDocument(Document):
    investor_identifier = fields.IntegerField(attr="id")

    class Django:
        model = Investor
        exclude = ["involvements"]

    def prepare_country(self, instance: Investor):
        if instance.country:
            return {
                "id": instance.country.id,
                "name": instance.country.name,
            }

    class Index:
        name = "investor"


@registry.register_document
class InvolvementDocument(Document):
    class Django:
        model = InvestorVentureInvolvement
        exclude = []

    class Index:
        name = "involvement"
