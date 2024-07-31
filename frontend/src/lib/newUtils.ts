import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { Version2Status } from "$lib/types/data"

type VersionStatusMap = {
  [key in Version2Status | "DELETED" | "REACTIVATED"]: {
    title: string
    classes: string
  }
}

export const stateMap = derived(
  _,
  ($_): VersionStatusMap => ({
    DRAFT: { title: $_("Draft"), classes: "text-black bg-green-300" },
    REVIEW: { title: $_("Review"), classes: "text-black bg-green-400" },
    ACTIVATION: { title: $_("Activation"), classes: "text-black bg-green-500" },
    ACTIVATED: { title: $_("Activated"), classes: "text-white bg-green-700" },
    // FIXME: still used in workflowinfos
    DELETED: { title: $_("Deleted"), classes: "text-white bg-red-500" },
    REACTIVATED: { title: $_("Activated"), classes: "text-white bg-green-700" },
  }),
)
