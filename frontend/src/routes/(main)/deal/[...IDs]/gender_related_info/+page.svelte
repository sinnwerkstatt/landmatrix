<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version
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
