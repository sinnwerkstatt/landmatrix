<script lang="ts">
  import { slide } from "svelte/transition"

  import type { DealHull } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  import ComplexPriceEditField from "./ComplexPriceEditField.svelte"

  export let deal: DealHull

  $: version = deal.selected_version
</script>

<form id="general" class="pb-52">
  <EditSubsection id="land_area">
    <EditField bind:value={version.intended_size} fieldname="intended_size" showLabel />
    <EditField bind:value={version.contract_size} fieldname="contract_size" showLabel />
    <EditField
      bind:value={version.production_size}
      fieldname="production_size"
      showLabel
    />
    <EditField
      bind:value={version.land_area_comment}
      fieldname="land_area_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="intention_of_investment">
    <EditField
      bind:value={version.intention_of_investment}
      fieldname="intention_of_investment"
      showLabel
    />
    <EditField
      bind:value={version.intention_of_investment_comment}
      fieldname="intention_of_investment_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="carbon_offset_project">
    <EditField
      bind:value={version.carbon_offset_project}
      fieldname="carbon_offset_project"
      showLabel
    />
    <EditField
      bind:value={version.carbon_offset_project_comment}
      fieldname="carbon_offset_project_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="nature_of_deal">
    <EditField
      bind:value={version.nature_of_deal}
      fieldname="nature_of_deal"
      showLabel
    />
    <EditField
      bind:value={version.nature_of_deal_comment}
      fieldname="nature_of_deal_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="negotiation_status">
    <EditField
      bind:value={version.negotiation_status}
      fieldname="negotiation_status"
      showLabel
    />
    <EditField
      bind:value={version.negotiation_status_comment}
      fieldname="negotiation_status_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="implementation_status">
    <EditField
      bind:value={version.implementation_status}
      fieldname="implementation_status"
      showLabel
    />
    <EditField
      bind:value={version.implementation_status_comment}
      fieldname="implementation_status_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="purchase_price">
    <ComplexPriceEditField
      bind:version
      fields={[
        "purchase_price",
        "purchase_price_currency",
        "purchase_price_type",
        "purchase_price_area",
      ]}
    />

    <EditField
      bind:value={version.purchase_price_comment}
      fieldname="purchase_price_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="leasing_fee">
    <ComplexPriceEditField
      bind:version
      fields={[
        "annual_leasing_fee",
        "annual_leasing_fee_currency",
        "annual_leasing_fee_type",
        "annual_leasing_fee_area",
      ]}
    />

    <EditField
      bind:value={version.annual_leasing_fee_comment}
      fieldname="annual_leasing_fee_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="contract_farming">
    <EditField
      bind:value={version.contract_farming}
      fieldname="contract_farming"
      showLabel
    />
    {#if version.contract_farming === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="on_the_lease_state"
          bind:value={version.on_the_lease_state}
          showLabel
        />
        {#if version.on_the_lease_state === true}
          <div class="pl-4" transition:slide={{ duration: 300 }}>
            <EditField
              fieldname="on_the_lease"
              bind:value={version.on_the_lease}
              showLabel
            />
          </div>
        {/if}
        <EditField
          fieldname="off_the_lease_state"
          bind:value={version.off_the_lease_state}
          showLabel
        />
        {#if version.off_the_lease_state === true}
          <div class="pl-4" transition:slide={{ duration: 300 }}>
            <EditField
              fieldname="off_the_lease"
              bind:value={version.off_the_lease}
              showLabel
            />
          </div>
        {/if}
      </div>
    {/if}
    <EditField
      bind:value={version.contract_farming_comment}
      fieldname="contract_farming_comment"
      showLabel
    />
  </EditSubsection>
</form>
