from apps.grid.forms.deal_action_comment_form import DealActionCommentForm
from apps.grid.forms.deal_contract_form import DealContractFormSet, PublicViewDealContractFormSet
from apps.grid.forms.deal_data_source_form import AddDealDataSourceFormSet, PublicViewDealDataSourceFormSet
from apps.grid.forms.deal_employment_form import DealEmploymentForm
from apps.grid.forms.deal_former_use_form import DealFormerUseForm
from apps.grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from apps.grid.forms.deal_general_form import DealGeneralForm
from apps.grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from apps.grid.forms.deal_overall_comment_form import DealOverallCommentForm
from apps.grid.forms.deal_produce_info_form import DealProduceInfoForm, PublicViewDealProduceInfoForm
from apps.grid.forms.deal_spatial_form import DealSpatialFormSet, PublicViewDealSpatialFormSet
from apps.grid.forms.deal_vggt_form import DealVGGTForm
from apps.grid.forms.deal_water_form import DealWaterForm
from apps.grid.forms.operational_stakeholder_form import OperationalStakeholderForm

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
