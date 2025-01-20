<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="investor_info" class="pb-52">
  <EditSubsection id="operating_company">
    <!-- TODO Later we're using operating_company instead of operating_company_id because of some DRF shit. IF you want, try and fix it.  -->
    <EditField
      bind:value={deal.selected_version.operating_company}
      fieldname="operating_company"
      showLabel
    />

    <EditField
      bind:value={deal.selected_version.involved_actors}
      fieldname="involved_actors"
      showLabel
    />

    <EditField
      bind:value={deal.selected_version.project_name}
      fieldname="project_name"
      showLabel
    />

    <EditField
      bind:value={deal.selected_version.investment_chain_comment}
      fieldname="investment_chain_comment"
      showLabel
    />
  </EditSubsection>
</form>
