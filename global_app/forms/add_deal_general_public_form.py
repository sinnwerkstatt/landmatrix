from global_app.forms.add_deal_general_form import AddDealGeneralForm

from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AddDealGeneralPublicForm(AddDealGeneralForm):

    form_title = _('General Info')

    class Meta:

        fields = (
            "tg_land_area", "intended_size", "tg_land_area_comment",
            "tg_intention", "intention", "tg_intention_comment",
            "tg_implementation_status", "implementation_status", "tg_implementation_status_comment",
            "tg_negotiation_status", "negotiation_status", "tg_negotiation_status_comment",
            "tg_purchase_price", "purchase_price", "purchase_price_currency", "purchase_price_type", "purchase_price_area", "tg_purchase_price_comment",
            )
