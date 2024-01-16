<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import InvestorLinkField from "$components/Fields/Display2/InvestorLinkField.svelte"
  import JSONActorsField from "$components/Fields/Display2/JSONActorsField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import InvolvementsGraph from "$components/New/InvolvementsGraph/InvolvementsGraph.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Operating Company")}
    fields={[
      version.operating_company_id,
      version.involved_actors,
      version.project_name,
      version.investment_chain_comment,
    ]}
  >
    <InvestorLinkField
      fieldname="operating_company"
      label={$_("Operating Company")}
      value={version.operating_company_id}
    />

    <JSONActorsField
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
  {#if version.operating_company_id}
    <h3 class="heading5 mb-6 mt-8">
      {$_("Network of parent companies and tertiary investors/lenders")}
    </h3>
    <InvolvementsGraph
      investor_id={version.operating_company_id}
      skipVentures
      hideControls
    />
  {/if}
</section>
