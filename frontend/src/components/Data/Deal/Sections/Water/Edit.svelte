<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="water" class="pb-52">
  <EditSubsection id="water_extraction_envisaged">
    <EditField
      bind:value={deal.selected_version.water_extraction_envisaged}
      fieldname="water_extraction_envisaged"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.water_extraction_envisaged_comment}
      fieldname="water_extraction_envisaged_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="source_of_water_extraction">
    <EditField
      bind:value={deal.selected_version.source_of_water_extraction}
      fieldname="source_of_water_extraction"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.source_of_water_extraction_comment}
      fieldname="source_of_water_extraction_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="how_much_do_investors_pay_comment">
    <EditField
      bind:value={deal.selected_version.how_much_do_investors_pay_comment}
      fieldname="how_much_do_investors_pay_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="water_extraction_amount">
    <EditField
      bind:value={deal.selected_version.water_extraction_amount}
      fieldname="water_extraction_amount"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.water_extraction_amount_comment}
      fieldname="water_extraction_amount_comment"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.use_of_irrigation_infrastructure}
      fieldname="use_of_irrigation_infrastructure"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.use_of_irrigation_infrastructure_comment}
      fieldname="use_of_irrigation_infrastructure_comment"
      showLabel
    />
    <EditField
      bind:value={deal.selected_version.water_footprint}
      fieldname="water_footprint"
      showLabel
    />
  </EditSubsection>
</form>
