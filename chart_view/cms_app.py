__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ChartViewApphook(CMSApp):
    name = _("Chart View")
    urls = ["chart_view.urls"]

apphook_pool.register(ChartViewApphook)
