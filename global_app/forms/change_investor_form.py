__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.add_investor_form import AddInvestorForm


class ChangeInvestorForm(AddInvestorForm):

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        data = super().get_data(object, tg, prefix)
        return data
