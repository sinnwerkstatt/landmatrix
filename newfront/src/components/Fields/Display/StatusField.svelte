<script lang="ts">
  import { _ } from "svelte-i18n";

  const combined_status_fn = (
    status: number,
    draft_status: number | null,
    toString = false
  ): string => {
    if (status === 4) return toString ? "Deleted" : "DELETED";
    if (draft_status === 1) return toString ? "Draft" : "DRAFT";
    if (draft_status === 2) return toString ? "Submitted for review" : "REVIEW";
    if (draft_status === 3) return toString ? "Submitted for activation" : "ACTIVATION";
    if (draft_status === 4) return toString ? "Rejected" : "REJECTED";
    if (draft_status === 5) return toString ? "To Delete" : "TO_DELETE";
    if ([2, 3].includes(status) && draft_status === null)
      return toString ? "Active" : "ACTIVE";
    throw Error(`Invalid status ${status} ${draft_status}`);
  };

  export let status: number;
  export let draft_status: number;
  $: display_status = $_(combined_status_fn(status, draft_status, true));
</script>

<span class="status_field">{display_status}</span>
