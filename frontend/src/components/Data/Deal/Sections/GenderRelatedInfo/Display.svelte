<script lang="ts">
  import type { DealHull, DealVersion2 } from "$lib/types/data"

  import Subsection from "$components/Data/Subsection.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()

  let version: DealVersion2 = $state(deal.selected_version)
</script>

<section>
  <Subsection id="gender_related_information" obj={version}>
    <DisplayField
      fieldname="gender_related_information"
      showLabel
      value={version.gender_related_information}
    />
  </Subsection>
</section>
