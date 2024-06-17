<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let deal: DealHull
  $: version = deal.selected_version
</script>

<form id="former_use" class="pb-52">
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
