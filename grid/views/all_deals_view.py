from grid.views.table_group_view import TableGroupView




class AllDealsView(TableGroupView):
    template_name = "all_deals.html"

    def dispatch(self, request, *args, **kwargs):
        kwargs["group"] = "all"
        return super(AllDealsView, self).dispatch(request, *args, **kwargs)
