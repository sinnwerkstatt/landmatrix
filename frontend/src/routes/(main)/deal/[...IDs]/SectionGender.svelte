<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
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
