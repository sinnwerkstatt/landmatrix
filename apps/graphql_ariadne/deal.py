from apps.greennewdeal.documents import DealDocument
from apps.greennewdeal.models import Deal


def resolve_deal(*_, id):
    return list(DealDocument.search().filter("term", id=id))[0]


def resolve_deals(*_):
    return list(DealDocument.search())
    # return [d.to_json() for d in Deal.objects.all()]
