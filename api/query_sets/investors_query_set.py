from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from landmatrix.models.investor import Investor
from django.core.paginator import Paginator

# TODO: investors is a standard model, use a real queryset


class InvestorsQuerySet(SimpleFakeQuerySet):
    def all(self):
        investors = Investor.objects.all()
        term = self.get_data.GET.get('q', '')
        if term:
            investors = investors.filter(name__icontains=term)
        #role = self.get_data.GET.get('role', '')
        #if role == 'operational_stakeholder':
        #    investors = investors.filter(investoractivityinvolvement__isnull=False)
        #else:
        #    investors = investors.filter(investoractivityinvolvement__isnull=True)
        investors = investors.order_by('name')
        return [
                {'id': investor.id, 'text': investor.name.strip()}
                for investor in investors
        ]