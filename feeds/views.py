from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from landmatrix.models.deal import Deal
from .deal_changes import DealChangesList


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
            'timestamp': item[0],
            'deal': item[1],
            'changes': item[2],
        })

        return context

    def items(self, obj):
        deal_changes = DealChangesList(obj, max_items=self.max_items)

        return deal_changes

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
        timestamp, deal, changes = item
        deal_timestamp = int(timestamp.timestamp())
        compound_id = '{0}_{1:d}'.format(deal.id, deal_timestamp)
        url = reverse('deal_detail', kwargs={'deal_id': compound_id})

        return url

    def item_pubdate(self, item):
        timestamp, deal, changes = item

        return timestamp

    def item_author_name(self, item):
        timestamp, deal, changes = item
        try:
            name = deal.activity.history_user.name
        except AttributeError:
            name = None

        return name

    def item_author_email(self, item):
        timestamp, deal, changes = item
        try:
            email = deal.activity.history_user.email
        except AttributeError:
            email = None

        return email
