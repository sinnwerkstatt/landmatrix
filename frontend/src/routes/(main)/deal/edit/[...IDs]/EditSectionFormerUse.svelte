<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let version: DealVersion2
</script>

<form id="former_use">
  <EditSubsection id="former_land_owner">
    <EditField
      bind:value={version.former_land_owner}
      fieldname="former_land_owner"
      showLabel
    />
    <EditField
      bind:value={version.former_land_owner_comment}
      fieldname="former_land_owner_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="former_land_use">
    <EditField
      bind:value={version.former_land_use}
      fieldname="former_land_use"
      showLabel
    />
    <EditField
      bind:value={version.former_land_use_comment}
      fieldname="former_land_use_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="former_land_cover">
    <EditField
      bind:value={version.former_land_cover}
      fieldname="former_land_cover"
      showLabel
    />
    <EditField
      bind:value={version.former_land_cover_comment}
      fieldname="former_land_cover_comment"
      showLabel
    />
  </EditSubsection>
</form>
