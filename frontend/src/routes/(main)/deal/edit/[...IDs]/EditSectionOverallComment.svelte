<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Edit2/TextField.svelte"

  import EditSubsection from "./EditSubsection.svelte"

  export let deal: DealHull
</script>

<form id="overall_comment">
  <EditSubsection>
    <TextField
      bind:value={deal.selected_version.overall_comment}
      fieldname="overall_comment"
      label={$_("Overall comment")}
      multiline
    />
  </EditSubsection>
</form>
