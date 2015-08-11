__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.add_deal_general_form import AddDealGeneralForm


class PublicViewDealGeneralForm(AddDealGeneralForm):

    class Meta:
        fields = (
            "tg_land_area", "intended_size", "contract_size", "production_size",
            "tg_intention", "intention",
            "tg_nature", "nature",
            "tg_negotiation_status", "negotiation_status",
            "tg_implementation_status", "implementation_status",
            "tg_contract_farming", "contract_farming",
        )
        readonly_fields = (
            "tg_land_area", "intended_size", "contract_size", "production_size",
            "tg_intention", "intention",
            "tg_nature", "nature",
            "tg_negotiation_status", "negotiation_status",
            "tg_implementation_status", "implementation_status",
            "tg_contract_farming", "contract_farming",
        )
