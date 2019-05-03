from django.template import loader
from django.http import HttpResponse

from grid.forms.deal_action_comment_form import DealActionCommentForm
from grid.forms.deal_contract_form import PublicViewDealContractFormSet, DealContractFormSet
from grid.forms.deal_data_source_form import PublicViewDealDataSourceFormSet, AddDealDataSourceFormSet
from grid.forms.deal_employment_form import DealEmploymentForm
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_general_form import DealGeneralForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_overall_comment_form import DealOverallCommentForm
from grid.forms.deal_produce_info_form import PublicViewDealProduceInfoForm, DealProduceInfoForm
from grid.forms.deal_spatial_form import PublicViewDealSpatialFormSet, DealSpatialFormSet
from grid.forms.deal_vggt_form import DealVGGTForm
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm

DEAL_FORMS = [
    DealSpatialFormSet,
    DealGeneralForm,
    DealContractFormSet,
    DealEmploymentForm,
    OperationalStakeholderForm,
    AddDealDataSourceFormSet,
    DealLocalCommunitiesForm,
    DealFormerUseForm,
    DealProduceInfoForm,
    DealWaterForm,
    DealGenderRelatedInfoForm,
    DealVGGTForm,
    DealOverallCommentForm,
    DealActionCommentForm,
]

PUBLIC_FORMS = [
    ("location", PublicViewDealSpatialFormSet),
    ("general_information", DealGeneralForm),
    ("contracts", PublicViewDealContractFormSet),
    ("employment", DealEmploymentForm),
    ("investor_info", OperationalStakeholderForm),
    ("data_sources", PublicViewDealDataSourceFormSet),
    ("local_communities", DealLocalCommunitiesForm),
    ("former_use", DealFormerUseForm),
    ("produce_info", PublicViewDealProduceInfoForm),
    ("water", DealWaterForm),
    ("gender-related_info", DealGenderRelatedInfoForm),
    ("vggt", DealVGGTForm),
    ("overall_comment", DealOverallCommentForm),
]
USER_FORMS = [
    ("action_comment", DealActionCommentForm),
]
