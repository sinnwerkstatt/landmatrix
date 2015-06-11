__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class GlobalApphook(CMSApp):
    name = _("Global")
    urls = ["global.urls"]

apphook_pool.register(GlobalApphook)
