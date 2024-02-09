<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let version: DealVersion2
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
