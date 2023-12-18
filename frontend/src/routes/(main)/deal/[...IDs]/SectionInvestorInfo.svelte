<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Operating Company")}
    fields={[
      version.operating_company,
      version.involved_actors,
      version.project_name,
      version.investment_chain_comment,
    ]}
  >
    <TextField
      fieldname="operating_company"
      label={$_("Operating Company")}
      value={version.operating_company.name}
    />
    <TextField
      fieldname="involved_actors"
      label={$_("Comment on investment chain ")}
      value={version.involved_actors}
    />
    <TextField
      fieldname="project_name"
      label={$_("Comment on investment chain ")}
      value={version.project_name}
    />
    <TextField
      fieldname="investment_chain_comment"
      label={$_("Comment on investment chain ")}
      value={version.investment_chain_comment}
    />
  </Subsection>
</section>
