<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import InvestorForeignKey from "$components/Fields/Edit2/InvestorForeignKey.svelte"
  import JSONActorsField from "$components/Fields/Edit2/JSONActorsField.svelte"
  import TextField from "$components/Fields/Edit2/TextField.svelte"

  import EditSubsection from "./EditSubsection.svelte"

  export let deal: DealHull
  $: version = deal.selected_version
  // export let version: DealVersion2
</script>

<form id="investor_info">
  <EditSubsection title={$_("Operating company")}>
    <InvestorForeignKey
      bind:value={version.operating_company}
      label={$_("Operating company")}
    />

    <JSONActorsField
      bind:value={version.involved_actors}
      label={$_("Actors involved in the negotiation / admission process")}
    />
    <TextField
      bind:value={version.project_name}
      fieldname="project_name"
      label={$_("Name of investment project")}
    />
    <TextField
      bind:value={version.investment_chain_comment}
      fieldname="investment_chain_comment"
      label={$_("Comment on investment chain")}
      multiline
    />
  </EditSubsection>
</form>
