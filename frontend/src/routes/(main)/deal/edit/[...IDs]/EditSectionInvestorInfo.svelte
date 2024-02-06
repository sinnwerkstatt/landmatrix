<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import InvestorForeignKey from "$components/Fields/Edit2/InvestorForeignKey.svelte"
  import JSONActorsEditField from "$components/Fields/Edit2/JSONActorsEditField.svelte"
  import TextEditField from "$components/Fields/Edit2/TextEditField.svelte"

  export let deal: DealHull
  $: version = deal.selected_version
  // export let version: DealVersion2
</script>

<form id="investor_info">
  <EditSubsection id="operating_company">
    <InvestorForeignKey
      bind:value={version.operating_company}
      label={$_("Operating company")}
    />

    <JSONActorsEditField
      bind:value={version.involved_actors}
      label={$_("Actors involved in the negotiation / admission process")}
    />
    <TextEditField
      bind:value={version.project_name}
      fieldname="project_name"
      label={$_("Name of investment project")}
    />
    <TextEditField
      bind:value={version.investment_chain_comment}
      fieldname="investment_chain_comment"
      label={$_("Comment on investment chain")}
      multiline
    />
  </EditSubsection>
</form>
