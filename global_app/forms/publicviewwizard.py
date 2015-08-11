from global_app.forms import *
from global_app.forms.deal_spatial_form import DealSpatialForm

"""
Readonly and limited to the following fields:
#ID
#Target Country
#Location
Investor names
Investor countries
#Intention of investment
#Negotiation Status + years
#Implementation Status + years
#Investment size: Intended, under contract, under production
#Nature of the deal
#Data sources including links and types.
#For Personal information including "organization"
#Contract farming
Crops
"""

class PublicViewDealSpatialForm(DealSpatialForm):

    class Meta:
        fields = (
            "tg_location", "location", "point_lat", "point_lon",
        )
        readonly_fields = (
            "tg_location", "location", "point_lat", "point_lon",
        )
PublicViewDealSpatialFormSet = formset_factory(PublicViewDealSpatialForm, formset=AddDealSpatialFormSet, extra=0)

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

class PublicViewDealDataSourceForm(DealDataSourceForm):

    class Meta:
        fields = (
            "tg_data_source", "type", "url", "company", "date"
        )
        readonly_fields = (
            "tg_data_source", "type", "url", "company", "date"
        )
PublicViewDealDataSourceFormSet = formset_factory(PublicViewDealDataSourceForm, formset=AddDealDataSourceFormSet, extra=0)

class PublicViewDealProduceInfoForm(DealProduceInfoForm):

    class Meta:
        fields = (
            "tg_crop_animal_mineral", "crops",
        )
        readonly_fields = (
            "tg_crop_animal_mineral", "crops",
        )
