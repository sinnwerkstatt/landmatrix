<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let version: DealVersion2
</script>

<form id="gender_related_info">
  <EditSubsection id="gender_related_information">
    <EditField
      bind:value={version.gender_related_information}
      fieldname="gender_related_information"
      showLabel
    />
  </EditSubsection>
</form>
