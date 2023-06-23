import { writable, derived } from "svelte/store"
import { _ } from "svelte-i18n"

import type { User } from "$lib/types/user"
import type { Country } from "$lib/types/wagtail"

export enum Mode {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  ACTIVATION = "ACTIVATION",
  ACTIVE = "ACTIVE",
  REJECTED = "REJECTED",
  DELETED = "DELETED",
}
export const MODES: Mode[] = Object.values(Mode)

type ModeMap = { [key in Mode]: string }
export const modeMap = derived(
  _,
  ($_): ModeMap => ({
    DRAFT: $_("Draft"),
    REVIEW: $_("Review"),
    ACTIVATION: $_("Activation"),
    ACTIVE: $_("Active"),
    REJECTED: $_("Rejected"),
    DELETED: $_("Deleted"),
  }),
)

export interface ManagementFilters {
  mode?: Mode
  country?: Country
  dealSizeFrom?: number
  dealSizeTo?: number
  createdAtFrom?: Date
  createdAtTo?: Date
  createdBy?: User
  modifiedAtFrom?: Date
  modifiedAtTo?: Date
  modifiedBy?: User
  fullyUpdatedAtFrom?: Date
  fullyUpdatedAtTo?: Date
}

export const managementFilters = writable<ManagementFilters>({})
