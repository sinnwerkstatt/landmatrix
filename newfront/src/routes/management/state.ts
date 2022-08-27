import { writable } from "svelte/store";
import type { User } from "$lib/types/user";
import type { Country } from "$lib/types/wagtail";

interface ManagementFilters {
  country?: Country;
  dealSizeFrom?: number;
  dealSizeTo?: number;
  createdAtFrom?: Date;
  createdAtTo?: Date;
  createdBy?: User;
  modifiedAtFrom?: Date;
  modifiedAtTo?: Date;
  modifiedBy?: User;
}

export const managementFilters = writable<ManagementFilters>({});
