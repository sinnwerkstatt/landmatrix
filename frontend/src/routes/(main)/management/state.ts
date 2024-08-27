import { writable } from "svelte/store"

import type { components } from "$lib/openAPI"
import type { Version2Status } from "$lib/types/data"

export interface ManagementFilters {
  status?: Version2Status
  country?: components["schemas"]["Country"]
  dealSizeFrom?: number
  dealSizeTo?: number
  createdAtFrom?: Date
  createdAtTo?: Date
  createdByID?: number
  modifiedAtFrom?: Date
  modifiedAtTo?: Date
  modifiedByID?: number
  fullyUpdatedAtFrom?: Date
  fullyUpdatedAtTo?: Date
}

export const managementFilters = writable<ManagementFilters>({})
