import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import { flatIoIChoices, IoIGroupChoices } from "$lib/choices"
import {
  ImplementationStatus,
  IntentionOfInvestmentGroup,
  NegotiationStatusGroup,
  type AreaType,
  type IntentionOfInvestment,
} from "$lib/types/deal"

type ImplementationStatusMap = { [key in ImplementationStatus]: string }
export const implementationStatusMap = derived(
  _,
  ($_): ImplementationStatusMap => ({
    [ImplementationStatus.PROJECT_NOT_STARTED]: $_("Project not started"),
    [ImplementationStatus.STARTUP_PHASE]: $_("Startup phase (no production)"),
    [ImplementationStatus.IN_OPERATION]: $_("In operation (production)"),
    [ImplementationStatus.PROJECT_ABANDONED]: $_("Project abandoned"),
  }),
)

type NegotiationStatusGroupMap = { [key in NegotiationStatusGroup]: string }
export const negotiationStatusGroupMap = derived(
  _,
  ($_): NegotiationStatusGroupMap => ({
    [NegotiationStatusGroup.INTENDED]: $_("Intended"),
    [NegotiationStatusGroup.CONCLUDED]: $_("Concluded"),
    [NegotiationStatusGroup.FAILED]: $_("Failed"),
    [NegotiationStatusGroup.CONTRACT_EXPIRED]: $_("Contract expired"),
  }),
)

type IntentionOfInvestmentGroupMap = { [key in IntentionOfInvestmentGroup]: string }
export const intentionOfInvestmentGroupMap = derived(
  _,
  ($_): IntentionOfInvestmentGroupMap =>
    Object.fromEntries(
      Object.entries(IoIGroupChoices).map(([key, value]) => [key, $_(value)]),
    ) as IntentionOfInvestmentGroupMap,
)

type IntentionOfInvestmentMap = { [key in IntentionOfInvestment]: string }
export const intentionOfInvestmentMap = derived(
  _,
  ($_): IntentionOfInvestmentMap =>
    Object.fromEntries(
      Object.entries(flatIoIChoices).map(([key, value]) => [key, $_(value)]),
    ) as IntentionOfInvestmentMap,
)

type AreaTypeMap = { [key in AreaType]: string }
export const areaTypeMap = derived(
  _,
  ($_): AreaTypeMap => ({
    production_area: $_("Production area"),
    contract_area: $_("Contract area"),
    intended_area: $_("Intended area"),
  }),
)
