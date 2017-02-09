from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from .activity_changes import ActivityChangesList


class ActivityChangesFeed(Feed):
    ttl = 0  # TTL value for client side caching
    title_template = 'deal-change-title.html'
    description_template = 'deal-change-description.html'
    max_items = 100

    def get_object(self, request, deal_id=None):
        return deal_id

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
        changes = ActivityChangesList(obj, max_items=self.max_items)

        return changes

    def title(self, obj):
        title = _("Deal %(deal_id)s History") % {'deal_id': obj}

        return title

    def description(self, obj):
        description = _("A list of changes made to deal %(deal_id)s") % {
            'deal_id': obj,
        }

        return description

    def link(self, obj):
        url = reverse('deal_detail', kwargs={'deal_id': obj})

        return url

    def item_link(self, item):
        timestamp, activity, changes = item
        deal_url_kwargs = {
            'deal_id': activity.activity_identifier,
            'history_id': activity.id,
        }
        url = reverse('deal_detail', kwargs=deal_url_kwargs)

        return url

    def item_pubdate(self, item):
        timestamp, activity, changes = item

        return timestamp

    def item_author_name(self, item):
        timestamp, activity, changes = item
        try:
            name = activity.history_user.name
        except AttributeError:
            name = None

        return name

    def item_author_email(self, item):
        timestamp, activity, changes = item
        try:
            email = activity.history_user.email
        except AttributeError:
            email = None

        return email
