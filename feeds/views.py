from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from landmatrix.models import Activity, Deal


class DealChangesFeed(Feed):
    ttl = 0  # TTL value for client side caching
    title_template = 'deal-change-title.html'
    description_template = 'deal-change-description.html'
    max_items = 100

    def get_object(self, request, deal_id=None):
        return Activity.objects.get(activity_identifier=deal_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = kwargs.get('item', None)
        deal = Deal.from_activity(item) if item else None
        context.update({
            'activity': item,
            'deal': deal,
        })

        return context

    def items(self, obj):
        return obj.history.all()[:self.max_items]

    def title(self, obj):
        title = _("Deal %(deal_id)s History") % {
            'deal_id': obj.activity_identifier,
        }
        return title

    def description(self, obj):
        description = _("A list of changes made to deal %(deal_id)s") % {
            'deal_id': obj.activity_identifier,
        }
        return description

    def link(self, obj):
        url = reverse('deal_detail',
                      kwargs={'deal_id': obj.activity_identifier})

        return url

    def item_link(self, item):
        compound_id = '{0}_{1:d}'.format(
            item.activity_identifier, int(item.history_date.timestamp()))
        url = reverse('deal_detail', kwargs={'deal_id': compound_id})

        return url

    def item_pubdate(self, item):
        return item.history_date

    def item_author_name(self, item):
        return item.history_user.name if item.history_user else None

    def item_author_email(self, item):
        return item.history_user.email if item.history_user else None
