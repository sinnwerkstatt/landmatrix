<script lang="ts">
  import type { DealHull, DealVersion2 } from "$lib/types/data"

  import Subsection from "$components/Data/Subsection.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: DealHull

  let version: DealVersion2 = deal.selected_version
  $: version = deal.selected_version
</script>

<section>
  <Subsection id="former_land_owner" obj={version}>
    <DisplayField
      fieldname="former_land_owner"
      showLabel
      value={version.former_land_owner}
    />
    <DisplayField
      fieldname="former_land_owner_comment"
      showLabel
      value={version.former_land_owner_comment}
    />
  </Subsection>

  <Subsection id="former_land_use" obj={version}>
    <DisplayField
      fieldname="former_land_use"
      showLabel
      value={version.former_land_use}
    />
    <DisplayField
      fieldname="former_land_use_comment"
      showLabel
      value={version.former_land_use_comment}
    />
  </Subsection>

  <Subsection id="former_land_cover" obj={version}>
    <DisplayField
      fieldname="former_land_cover"
      showLabel
      value={version.former_land_cover}
    />
    <DisplayField
      fieldname="former_land_cover_comment"
      showLabel
      value={version.former_land_cover_comment}
    />
  </Subsection>
</section>
