<script lang="ts">
  import type { DealHull } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let deal: DealHull
  $: version = deal.selected_version
</script>

<form id="investor_info">
  <EditSubsection id="operating_company">
    <!-- TODO we're using operating_company instead of operating_company_id because of some DRF shit. IF you want, try and fix it.  -->
    <EditField
      bind:value={version.operating_company}
      fieldname="operating_company"
      showLabel
    />

    <EditField
      bind:value={version.involved_actors}
      fieldname="involved_actors"
      showLabel
    />

    <EditField bind:value={version.project_name} fieldname="project_name" showLabel />

    <EditField
      bind:value={version.investment_chain_comment}
      fieldname="investment_chain_comment"
      showLabel
    />
  </EditSubsection>
</form>
