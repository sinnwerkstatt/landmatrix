<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import CurrencyField from "$components/Fields/Edit2/CurrencyField.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let version: DealVersion2

  const PERTYPES = { PER_HA: $_("per ha"), PER_AREA: $_("for specified area") }
</script>

<form id="general">
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
      label={$_("Comment on negotiation status")}
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
    <EditField bind:value={version.purchase_price} fieldname="purchase_price" showLabel>
      <CurrencyField bind:value={version.purchase_price_currency} />
      <select bind:value={version.purchase_price_type} class="inpt">
        <option value={null}>----</option>
        <option value="PER_HA">{PERTYPES.PER_HA}</option>
        <option value="PER_AREA">{PERTYPES.PER_AREA}</option>
      </select>
    </EditField>

    <EditField
      bind:value={version.purchase_price_area}
      fieldname="purchase_price_area"
      showLabel
    />
    <EditField
      bind:value={version.purchase_price_comment}
      fieldname="purchase_price_comment"
      showLabel
    />
  </EditSubsection>

  <EditSubsection id="leasing_fee">
    <EditField
      bind:value={version.annual_leasing_fee}
      fieldname="annual_leasing_fee"
      showLabel
    >
      <CurrencyField bind:value={version.annual_leasing_fee_currency} />
      <select bind:value={version.annual_leasing_fee_type} class="inpt">
        <option value={null}>----</option>
        <option value="PER_HA">{PERTYPES.PER_HA}</option>
        <option value="PER_AREA">{PERTYPES.PER_AREA}</option>
      </select>
    </EditField>
    <EditField
      bind:value={version.annual_leasing_fee_area}
      fieldname="annual_leasing_fee_area"
      showLabel
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
