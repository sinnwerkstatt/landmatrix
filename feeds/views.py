from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from grid.views.deal_comparison_view import get_comparison
from landmatrix.models import Activity, Deal


def get_deals_with_changes(initial_deal, activity_history):
    deals = []
    # we're going backwards through history here
    later_deal = initial_deal
    for activity in activity_history:
        current_deal = Deal.from_activity(activity)
        form_comparison = get_comparison(later_deal, current_deal)
        deals.append((activity, later_deal, form_comparison))
        later_deal = current_deal

    return deals


class DealChangesFeed(Feed):
    ttl = 0  # TTL value for client side caching
    title_template = 'deal-change-title.html'
    description_template = 'deal-change-description.html'
    max_items = 100

    def get_object(self, request, deal_id=None):
        return Deal(deal_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = kwargs.get('item', None)
        context.update({
            'activity': item[0],
            'deal': item[1],
            'forms': item[2],
        })

        return context

    def items(self, obj):
        '''
        Returns a list of (deal, [(form1, form2, different), ...]) tuples.
        '''
        activity_history = obj.activity.history.all()[:self.max_items]
        items = get_deals_with_changes(obj, activity_history)

        return items

    def title(self, obj):
        title = _("Deal %(deal_id)s History") % {'deal_id': obj.id}

        return title

    def description(self, obj):
        description = _("A list of changes made to deal %(deal_id)s") % {
            'deal_id': obj.id,
        }

        return description

    def link(self, obj):
        url = reverse('deal_detail', kwargs={'deal_id': obj.id})

        return url

    def item_link(self, item):
        activity, deal, form_comparison = item
        compound_id = '{0}_{1:d}'.format(
            deal.id, int(activity.history_date.timestamp()))
        url = reverse('deal_detail', kwargs={'deal_id': compound_id})

        return url

    def item_pubdate(self, item):
        activity, deal, form_comparison = item

        return activity.history_date

    def item_author_name(self, item):
        activity, deal, form_comparison = item

        return activity.history_user.name if activity.history_user else None

    def item_author_email(self, item):
        activity, deal, form_comparison = item
        author = deal.activity.history_user

        return activity.history_user.email if activity.history_user else None
