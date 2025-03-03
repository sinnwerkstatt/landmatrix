<script lang="ts">
  import type { DealHull, DealVersion } from "$lib/types/data"

  import Subsection from "$components/Data/Subsection.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()

  let version: DealVersion = $state(deal.selected_version)
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
