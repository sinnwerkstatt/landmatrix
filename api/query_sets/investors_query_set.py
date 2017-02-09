from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from landmatrix.models.investor import Investor, InvestorActivityInvolvement



# TODO: investors is a standard model, use a real queryset


class InvestorsQuerySet(SimpleFakeQuerySet):
    def all(self):
        investors = Investor.objects.filter(
            pk__in=InvestorActivityInvolvement.objects.values('fk_investor_id').distinct()
        ).filter(name__icontains=self.get_data.GET.get('q', '')).order_by('name')
        return [
            {'id': investor.id, 'text': investor.name}
            for investor in investors
        ]
