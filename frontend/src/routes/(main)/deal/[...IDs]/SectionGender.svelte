<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Any gender-specific information about the investment and its impacts")}
    fields={[version.gender_related_information]}
  >
    <TextField
      fieldname="gender_related_information"
      label={$_("Gender related information")}
      value={version.gender_related_information}
    />
  </Subsection>
</section>
