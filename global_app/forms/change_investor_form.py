__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.add_investor_form import AddInvestorForm


class ChangeInvestorForm(AddInvestorForm):

    @classmethod
    def get_data(cls, deal, tg=None, prefix=""):
        data = super().get_data(deal, tg, prefix)
        return data
