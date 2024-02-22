import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { Version2Status } from "$lib/types/newtypes"

// TODO Nuts can probably refactor this away. what about the "mode" thingies?

type VersionStatusMap = { [key in Version2Status]: { title: string; classes: string } }

export const stateMap = derived(
  _,
  ($_): VersionStatusMap => ({
    DRAFT: { title: $_("Draft"), classes: "text-black bg-green-300" },
    REVIEW: { title: $_("Review"), classes: "text-black bg-green-400" },
    ACTIVATION: { title: $_("Activation"), classes: "text-black bg-green-500" },
    ACTIVATED: { title: $_("Activated"), classes: "text-white bg-green-700" },
    REJECTED: { title: $_("Rejected"), classes: "bg-yellow-400" },
    TO_DELETE: { title: $_("Deleted"), classes: "text-white bg-red-500" },
    DELETED: { title: $_("Deleted"), classes: "text-white bg-red-500" },
  }),
)
