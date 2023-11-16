import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { DealVersion2Status } from "$lib/types/newtypes"

type VersionStatusMap = { [key in DealVersion2Status]: string }

export const stateMap = derived(
  _,
  ($_): VersionStatusMap => ({
    DRAFT: $_("Draft"),
    REVIEW: $_("Review"),
    ACTIVATION: $_("Activation"),
    ACTIVATED: $_("Activated"),
    REJECTED: $_("Rejected"),
    TO_DELETE: $_("Deleted"),
  }),
)
