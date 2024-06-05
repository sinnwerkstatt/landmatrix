<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let version: DealVersion2
</script>

<form id="overall_comment" class="pb-52">
  <EditSubsection id="overall_comment">
    <EditField
      bind:value={version.overall_comment}
      fieldname="overall_comment"
      showLabel
    />
  </EditSubsection>
</form>
