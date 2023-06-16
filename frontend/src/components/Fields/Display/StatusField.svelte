<script lang="ts">
  import { _ } from "svelte-i18n"

  import { DraftStatus, Status } from "$lib/types/generics"

  export let status: Status
  export let draft_status: DraftStatus | null
  export let toString = true

  $: combineStatus = (
    status: Status,
    draft_status: DraftStatus | null,
    toString = false,
  ): string => {
    if (status === Status.DELETED) return toString ? $_("Deleted") : "DELETED"
    if (draft_status === DraftStatus.DRAFT) return toString ? $_("Draft") : "DRAFT"
    if (draft_status === DraftStatus.REVIEW)
      return toString ? $_("Submitted for review") : "REVIEW"
    if (draft_status === DraftStatus.ACTIVATION)
      return toString ? $_("Submitted for activation") : "ACTIVATION"
    if (draft_status === DraftStatus.REJECTED)
      return toString ? $_("Rejected") : "REJECTED"
    if (draft_status === DraftStatus.TO_DELETE)
      return toString ? $_("To Delete") : "TO_DELETE"
    if ((status === Status.LIVE || status === Status.UPDATED) && draft_status === null)
      return toString ? $_("Active") : "ACTIVE"
    throw Error(`Invalid status ${status} ${draft_status}`)
  }
</script>

<span>{combineStatus(status, draft_status, toString)}</span>
