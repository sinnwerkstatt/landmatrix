import type { SvelteComponent } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { DealHull } from "$lib/types/newtypes"

import type { DealSection } from "./constants"
import ContractsDisplay from "./Contracts/Display.svelte"
import ContractsEdit from "./Contracts/Edit.svelte"
import DataSourcesDisplay from "./DataSources/Display.svelte"
import DataSourcesEdit from "./DataSources/Edit.svelte"
import EmploymentDisplay from "./Employment/Display.svelte"
import EmploymentEdit from "./Employment/Edit.svelte"
import FormerUseDisplay from "./FormerUse/Display.svelte"
import FormerUseEdit from "./FormerUse/Edit.svelte"
import GenderRelatedInfoDisplay from "./GenderRelatedInfo/Display.svelte"
import GenderRelatedInfoEdit from "./GenderRelatedInfo/Edit.svelte"
import GeneralInfoDisplay from "./General/Display.svelte"
import GeneralInfoEdit from "./General/Edit.svelte"
import HistoryDisplay from "./History/Display.svelte"
import InvestorInfoDisplay from "./InvestorInfo/Display.svelte"
import InvestorInfoEdit from "./InvestorInfo/Edit.svelte"
import LocalCommunitiesDisplay from "./LocalCommunities/Display.svelte"
import LocalCommunitiesEdit from "./LocalCommunities/Edit.svelte"
import LocationsDisplay from "./Locations/Display.svelte"
import LocationsEdit from "./Locations/Edit.svelte"
import OverallCommentDisplay from "./OverallComment/Display.svelte"
import OverallCommentEdit from "./OverallComment/Edit.svelte"
import ProduceInfoDisplay from "./ProduceInfo/Display.svelte"
import ProduceInfoEdit from "./ProduceInfo/Edit.svelte"
import WaterDisplay from "./Water/Display.svelte"
import WaterEdit from "./Water/Edit.svelte"

export interface SectionSpecs {
  label: string
  display: typeof SvelteComponent<{ deal: DealHull }>
  edit?: typeof SvelteComponent<{ deal: DealHull }>
}

export const dealSectionLookup = derived(
  [_],
  ([$_]): {
    [key in DealSection]: SectionSpecs
  } => ({
    general: {
      label: $_("General info"),
      display: GeneralInfoDisplay,
      edit: GeneralInfoEdit,
    },
    locations: {
      label: $_("Locations"),
      display: LocationsDisplay,
      edit: LocationsEdit,
    },
    contracts: {
      label: $_("Contracts"),
      display: ContractsDisplay,
      edit: ContractsEdit,
    },
    employment: {
      label: $_("Employment"),
      display: EmploymentDisplay,
      edit: EmploymentEdit,
    },
    "investor-info": {
      label: $_("Investor info"),
      display: InvestorInfoDisplay,
      edit: InvestorInfoEdit,
    },
    "data-sources": {
      label: $_("Data sources"),
      display: DataSourcesDisplay,
      edit: DataSourcesEdit,
    },
    "local-communities": {
      label: $_("Local communities / indigenous peoples"),
      display: LocalCommunitiesDisplay,
      edit: LocalCommunitiesEdit,
    },
    "former-use": {
      label: $_("Former use"),
      display: FormerUseDisplay,
      edit: FormerUseEdit,
    },
    "produce-info": {
      label: $_("Produce info"),
      display: ProduceInfoDisplay,
      edit: ProduceInfoEdit,
    },
    water: {
      label: $_("Water"),
      display: WaterDisplay,
      edit: WaterEdit,
    },
    "gender-related-info": {
      label: $_("Gender-related info"),
      display: GenderRelatedInfoDisplay,
      edit: GenderRelatedInfoEdit,
    },
    "overall-comment": {
      label: $_("Overall comment"),
      display: OverallCommentDisplay,
      edit: OverallCommentEdit,
    },
    history: {
      label: $_("Deal history"),
      display: HistoryDisplay,
    },
  }),
)
