__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.add_deal_employment_form import AddDealEmploymentForm


class DealEmploymentPublicForm(AddDealEmploymentForm):

    class Meta:

        fields = (
            "tg_foreign_jobs_created", "foreign_jobs_created", "foreign_jobs_planned", "tg_foreign_jobs_created_comment",
            "tg_domestic_jobs_created", "domestic_jobs_created", "domestic_jobs_planned", "tg_domestic_jobs_created_comment",
            )
