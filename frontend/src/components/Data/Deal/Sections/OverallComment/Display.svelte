<script lang="ts">
  import type { DealHull, DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let deal: DealHull

  let version: DealVersion2 = deal.selected_version
  $: version = deal.selected_version
</script>

<section>
  <Subsection id="overall_comment" obj={version}>
    <DisplayField
      fieldname="overall_comment"
      showLabel
      value={version.overall_comment}
    />
  </Subsection>
</section>
