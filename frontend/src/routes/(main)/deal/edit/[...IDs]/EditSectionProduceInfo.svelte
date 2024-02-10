<script lang="ts">
  import { slide } from "svelte/transition"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let version: DealVersion2
</script>

<form id="produce_info">
  <EditSubsection id="farming">
    <EditField fieldname="crops" showLabel bind:value={version.crops} />
    <EditField fieldname="crops_comment" showLabel bind:value={version.crops_comment} />
    <EditField fieldname="animals" showLabel bind:value={version.animals} />
    <EditField
      fieldname="animals_comment"
      showLabel
      bind:value={version.animals_comment}
    />
    <EditField
      fieldname="mineral_resources"
      showLabel
      bind:value={version.mineral_resources}
    />
    <EditField
      fieldname="mineral_resources_comment"
      showLabel
      bind:value={version.mineral_resources_comment}
    />
  </EditSubsection>

  <EditSubsection id="detailed_contract_farming">
    <EditField
      fieldname="contract_farming_crops"
      showLabel
      bind:value={version.contract_farming_crops}
    />
    <EditField
      fieldname="contract_farming_crops_comment"
      showLabel
      bind:value={version.contract_farming_crops_comment}
    />
    <EditField
      fieldname="contract_farming_animals"
      showLabel
      bind:value={version.contract_farming_animals}
    />
    <EditField
      fieldname="contract_farming_animals_comment"
      showLabel
      bind:value={version.contract_farming_animals_comment}
    />
  </EditSubsection>

  <EditSubsection id="electricity_generation">
    <EditField
      fieldname="electricity_generation"
      showLabel
      bind:value={version.electricity_generation}
    />
    <EditField
      fieldname="electricity_generation_comment"
      showLabel
      bind:value={version.electricity_generation_comment}
    />
  </EditSubsection>

  <EditSubsection id="carbon_sequestration">
    <EditField
      fieldname="carbon_sequestration"
      showLabel
      bind:value={version.carbon_sequestration}
    />
    <EditField
      fieldname="carbon_sequestration_comment"
      showLabel
      bind:value={version.carbon_sequestration_comment}
    />
  </EditSubsection>

  <EditSubsection id="use_of_produce">
    <EditField
      fieldname="has_domestic_use"
      showLabel
      bind:value={version.has_domestic_use}
    />
    {#if version.has_domestic_use === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="domestic_use"
          showLabel
          bind:value={version.domestic_use}
        />
      </div>
    {/if}
    <EditField fieldname="has_export" showLabel bind:value={version.has_export} />

    {#if version.has_export === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField fieldname="export" showLabel bind:value={version.export} />

        <EditField
          fieldname="export_country1"
          showLabel
          bind:value={version.export_country1}
        />
        <EditField
          fieldname="export_country1_ratio"
          showLabel
          bind:value={version.export_country1_ratio}
        />
        <EditField
          fieldname="export_country2"
          showLabel
          bind:value={version.export_country2}
        />
        <EditField
          fieldname="export_country2_ratio"
          showLabel
          bind:value={version.export_country2_ratio}
        />
        <EditField
          fieldname="export_country3"
          showLabel
          bind:value={version.export_country3}
        />
        <EditField
          fieldname="export_country3_ratio"
          showLabel
          bind:value={version.export_country3_ratio}
        />
      </div>
    {/if}
    <EditField
      fieldname="use_of_produce_comment"
      showLabel
      bind:value={version.use_of_produce_comment}
    />
  </EditSubsection>

  <EditSubsection id="in_country_processing">
    <EditField
      fieldname="in_country_processing"
      showLabel
      bind:value={version.in_country_processing}
    />
    <EditField
      fieldname="in_country_processing_comment"
      showLabel
      bind:value={version.in_country_processing_comment}
    />
    <EditField
      fieldname="in_country_processing_facilities"
      showLabel
      bind:value={version.in_country_processing_facilities}
    />
    <EditField
      fieldname="in_country_end_products"
      showLabel
      bind:value={version.in_country_end_products}
    />
  </EditSubsection>
</form>
