<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version
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
