import { writable } from "svelte/store"

import type { Version2Status } from "$lib/types/newtypes"
import type { User } from "$lib/types/user"
import type { Country } from "$lib/types/wagtail"

export interface ManagementFilters {
  status?: Version2Status
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
