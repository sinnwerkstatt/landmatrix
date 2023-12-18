<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection title={$_("Overall comment")} fields={[version.overall_comment]}>
    <TextField
      fieldname="overall_comment"
      label={$_("Overall comment")}
      value={version.overall_comment}
    />
  </Subsection>
</section>
