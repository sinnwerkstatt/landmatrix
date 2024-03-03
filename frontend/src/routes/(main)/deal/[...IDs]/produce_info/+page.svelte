<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version
</script>

<section>
  <Subsection id="farming" obj={version}>
    <DisplayField fieldname="crops" showLabel value={version.crops} />
    <DisplayField fieldname="crops_comment" showLabel value={version.crops_comment} />
    <DisplayField fieldname="animals" showLabel value={version.animals} />
    <DisplayField
      fieldname="animals_comment"
      showLabel
      value={version.animals_comment}
    />
    <DisplayField
      fieldname="mineral_resources"
      showLabel
      value={version.mineral_resources}
    />
    <DisplayField
      fieldname="mineral_resources_comment"
      showLabel
      value={version.mineral_resources_comment}
    />
  </Subsection>

  <Subsection id="detailed_contract_farming" obj={version}>
    <DisplayField
      fieldname="contract_farming_crops"
      showLabel
      value={version.contract_farming_crops}
    />
    <DisplayField
      fieldname="contract_farming_crops_comment"
      showLabel
      value={version.contract_farming_crops_comment}
    />
    <DisplayField
      fieldname="contract_farming_animals"
      showLabel
      value={version.contract_farming_animals}
    />
    <DisplayField
      fieldname="contract_farming_animals_comment"
      showLabel
      value={version.contract_farming_animals_comment}
    />
  </Subsection>

  <Subsection id="electricity_generation" obj={version}>
    <DisplayField
      fieldname="electricity_generation"
      showLabel
      value={version.electricity_generation}
    />
    <DisplayField
      fieldname="electricity_generation_comment"
      showLabel
      value={version.electricity_generation_comment}
    />
  </Subsection>

  <Subsection id="carbon_sequestration" obj={version}>
    <DisplayField
      fieldname="carbon_sequestration"
      showLabel
      value={version.carbon_sequestration}
    />
    <DisplayField
      fieldname="carbon_sequestration_comment"
      showLabel
      value={version.carbon_sequestration_comment}
    />
  </Subsection>

  <Subsection id="use_of_produce" obj={version}>
    <DisplayField
      fieldname="has_domestic_use"
      showLabel
      value={version.has_domestic_use}
    />
    <DisplayField fieldname="domestic_use" showLabel value={version.domestic_use} />
    <DisplayField fieldname="has_export" showLabel value={version.has_export} />
    <DisplayField fieldname="export" showLabel value={version.export} />
    <DisplayField
      fieldname="export_country1"
      showLabel
      value={version.export_country1}
    />
    <DisplayField
      fieldname="export_country1_ratio"
      showLabel
      value={version.export_country1_ratio}
    />
    <DisplayField
      fieldname="export_country2"
      showLabel
      value={version.export_country2}
    />
    <DisplayField
      fieldname="export_country2_ratio"
      showLabel
      value={version.export_country2_ratio}
    />
    <DisplayField
      fieldname="export_country3"
      showLabel
      value={version.export_country3}
    />
    <DisplayField
      fieldname="export_country3_ratio"
      showLabel
      value={version.export_country3_ratio}
    />
    <DisplayField
      fieldname="use_of_produce_comment"
      showLabel
      value={version.use_of_produce_comment}
    />
  </Subsection>

  <Subsection id="in_country_processing" obj={version}>
    <DisplayField
      fieldname="in_country_processing"
      showLabel
      value={version.in_country_processing}
    />
    <DisplayField
      fieldname="in_country_processing_comment"
      showLabel
      value={version.in_country_processing_comment}
    />
    <DisplayField
      fieldname="in_country_processing_facilities"
      showLabel
      value={version.in_country_processing_facilities}
    />
    <DisplayField
      fieldname="in_country_end_products"
      showLabel
      value={version.in_country_end_products}
    />
  </Subsection>
</section>
