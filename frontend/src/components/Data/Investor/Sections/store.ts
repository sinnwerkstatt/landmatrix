import type { SvelteComponent } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { InvestorHull } from "$lib/types/data"

import type { InvestorEditSection, InvestorSection } from "./constants"
import DataSourcesDisplay from "./DataSources/Display.svelte"
import DataSourcesEdit from "./DataSources/Edit.svelte"
import GeneralInfoDisplay from "./General/Display.svelte"
import GeneralInfoEdit from "./General/Edit.svelte"
import HistoryDisplay from "./History/Display.svelte"
import InvolvementsDisplay from "./Involvements/Display.svelte"
import ParentCompaniesEdit from "./Involvements/EditParentCompanies.svelte"
import TertiaryInvestorEdit from "./Involvements/EditTertiaryInvestors.svelte"
import NetworkGraphDisplay from "./NetworkGraph/Display.svelte"

export interface SectionSpecs {
  label: string
  display?: typeof SvelteComponent<{ investor: InvestorHull }>
  edit?: typeof SvelteComponent<{ investor: InvestorHull }>
}

export const investorSectionLookup = derived(
  [_],
  ([$_]): {
    [key in InvestorSection | InvestorEditSection]: SectionSpecs
  } => ({
    general: {
      label: $_("General info"),
      display: GeneralInfoDisplay,
      edit: GeneralInfoEdit,
    },
    involvements: {
      label: $_("Involvements"),
      display: InvolvementsDisplay,
    },
    "network-graph": {
      label: $_("Network graph"),
      display: NetworkGraphDisplay,
    },
    "data-sources": {
      label: $_("Data sources"),
      display: DataSourcesDisplay,
      edit: DataSourcesEdit,
    },
    history: {
      label: $_("Investor history"),
      display: HistoryDisplay,
    },
    "parent-companies": {
      label: $_("Parent companies"),
      edit: ParentCompaniesEdit,
    },
    "tertiary-investors": {
      label: $_("Tertiary investors/lenders"),
      edit: TertiaryInvestorEdit,
    },
  }),
)
