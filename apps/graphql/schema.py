import graphene
from graphene_django import DjangoObjectType

from apps.greennewdeal.models import Deal


class DealType(DjangoObjectType):
    class Meta:
        model = Deal


class Query(graphene.ObjectType):
    deals = graphene.List(DealType)
    deal = graphene.Field(DealType, id=graphene.Int(), name=graphene.String())

    def resolve_deals(self, info):
        return Deal.objects.all()

    def resolve_deal(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Deal.objects.get(pk=id)

        if name is not None:
            return Deal.objects.get(name=name)

        return None


schema = graphene.Schema(query=Query)
