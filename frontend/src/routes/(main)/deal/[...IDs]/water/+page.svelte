<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version
</script>

<section>
  <Subsection id="water_extraction_envisaged" obj={version}>
    <DisplayField
      fieldname="water_extraction_envisaged"
      showLabel
      value={version.water_extraction_envisaged}
    />
    <DisplayField
      fieldname="water_extraction_envisaged_comment"
      showLabel
      value={version.water_extraction_envisaged_comment}
    />
  </Subsection>

  <Subsection id="source_of_water_extraction" obj={version}>
    <DisplayField
      fieldname="source_of_water_extraction"
      showLabel
      value={version.source_of_water_extraction}
    />
    <DisplayField
      fieldname="source_of_water_extraction_comment"
      showLabel
      value={version.source_of_water_extraction_comment}
    />
  </Subsection>

  <Subsection id="how_much_do_investors_pay_comment" obj={version}>
    <DisplayField
      fieldname="how_much_do_investors_pay_comment"
      showLabel
      value={version.how_much_do_investors_pay_comment}
    />
  </Subsection>

  <Subsection id="water_extraction_amount" obj={version}>
    <DisplayField
      fieldname="water_extraction_amount"
      showLabel
      value={version.water_extraction_amount}
    />
    <DisplayField
      fieldname="water_extraction_amount_comment"
      showLabel
      value={version.water_extraction_amount_comment}
    />
    <DisplayField
      fieldname="use_of_irrigation_infrastructure"
      showLabel
      value={version.use_of_irrigation_infrastructure}
    />
    <DisplayField
      fieldname="use_of_irrigation_infrastructure_comment"
      showLabel
      value={version.use_of_irrigation_infrastructure_comment}
    />
    <DisplayField
      fieldname="water_footprint"
      showLabel
      value={version.water_footprint}
    />
  </Subsection>
</section>
