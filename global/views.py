
from django.views.generic import View

class AllDealsView(View):

    def dispatch(self, request, type, *args, **kwargs):
        kwargs["group"] = "all%s" % (type and type or "")
        return super(AllDealsView, self).dispatch(request, *args, **kwargs)
