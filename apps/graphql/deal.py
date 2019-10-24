from apps.greennewdeal.documents import DealDocument
from apps.greennewdeal.models import Deal


def resolve_deal(*_, id):
    DealDocument.search().query()
    debug
    d = Deal.objects.get(id=id)
    return d.to_json()
    # return Deal.objects.get(id=id).to_dict()


def resolve_deals(*_):
    return [d.to_json() for d in Deal.objects.all()]
