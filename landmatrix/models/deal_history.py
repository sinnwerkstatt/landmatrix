from global_app.views.view_aux_functions import render_to_string
from landmatrix.models.deal import Deal

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealHistoryItem(Deal):

    def get_timestamp(self):
        return self.activity.history_date

    def get_user(self):
        return self.activity.changed_by
