<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, DealVersion } from "$lib/types/data"

  import Subsection from "$components/Data/Subsection.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import InvolvementsGraph from "$components/New/InvolvementsGraph/InvolvementsGraph.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()

  let version: DealVersion = $state(deal.selected_version)
</script>

<section>
  <Subsection id="operating_company" obj={version}>
    <DisplayField
      fieldname="operating_company"
      value={version.operating_company_id}
      showLabel
    />
    <DisplayField
      fieldname="involved_actors"
      value={version.involved_actors}
      showLabel
    />
    <DisplayField fieldname="project_name" value={version.project_name} showLabel />
    <DisplayField
      fieldname="investment_chain_comment"
      value={version.investment_chain_comment}
      showLabel
    />
  </Subsection>

  {#if version.operating_company_id}
    <div class="heading4 mb-6 mt-8">
      {$_("Network of parent companies and tertiary investors/lenders")}
    </div>
    <div>{$_("Please click the nodes to get more details.")}</div>
    <InvolvementsGraph
      investorID={version.operating_company_id}
      skipVentures
      hideControls
    />
  {/if}
</section>
