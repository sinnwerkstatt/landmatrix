import { writable } from "svelte/store"

import type { components } from "$lib/openAPI"
import type { User, Version2Status } from "$lib/types/newtypes"

export interface ManagementFilters {
  status?: Version2Status
  country?: components["schemas"]["Country"]
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
