<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import DecimalField from "$components/Fields/Edit2/DecimalField.svelte"
  import JSONCurrentDateAreaField from "$components/Fields/Edit2/JSONCurrentDateAreaField.svelte"
  import TextField from "$components/Fields/Edit2/TextField.svelte"

  import EditSubsection from "./EditSubsection.svelte"

  export let deal: DealHull
  $: version = deal.selected_version
  // export let version: DealVersion2
</script>

<!--{JSON.stringify(version)}-->
<form id="general">
  <EditSubsection title={$_("Land area")}>
    <DecimalField
      bind:value={version.intended_size}
      fieldname="intended_size"
      label={$_("Intended size")}
      unit={$_("ha")}
    />
    <JSONCurrentDateAreaField
      fieldname="contract_size"
      bind:value={version.contract_size}
      label={$_("Size under contract (leased or purchased area)")}
    />
    <JSONCurrentDateAreaField
      fieldname="production_size"
      bind:value={version.production_size}
      label={$_("Size in operation (production)")}
    />
    <TextField
      bind:value={version.land_area_comment}
      fieldname="land_area_comment"
      label={$_("Comment on land area")}
    />
  </EditSubsection>
  <EditSubsection title={$_("Intention of investment")}>
    <!--    <JSONDateAreaChoicesField-->
    <!--      fieldname="intention_of_investment"-->
    <!--      bind:value={version.intention_of_investment}-->
    <!--      label={$_("Intention of investment")}-->
    <!--      choices={$fieldChoices.deal.intention_of_investment}-->
    <!--    />-->
    <TextField
      fieldname="intention_of_investment_comment"
      bind:value={version.intention_of_investment_comment}
      label={$_("Comment on intention of investment")}
    />
  </EditSubsection>

  <EditSubsection title={$_("Nature of the deal")}>
    <!--      <TextField-->
    <!--        fieldname="nature_of_deal"-->
    <!--        bind:value={version.nature_of_deal}-->
    <!--        label={$_("Nature of the deal")}-->
    <!--        choices={$fieldChoices.deal.nature_of_deal}-->
    <!--        multipleChoices-->
    <!--      />-->
    <TextField
      fieldname="nature_of_deal_comment"
      bind:value={version.nature_of_deal_comment}
      label={$_("Comment on nature of the deal")}
    />
  </EditSubsection>

  <EditSubsection title={$_("Negotiation status")}>
    <!--    <JSONCurrentDateChoiceField-->
    <!--      fieldname="negotiation_status"-->
    <!--      bind:value={version.negotiation_status}-->
    <!--      label={$_("Negotiation status")}-->
    <!--      choices={$fieldChoices.deal.negotiation_status}-->
    <!--    />-->
    <TextField
      fieldname="negotiation_status_comment"
      bind:value={version.negotiation_status_comment}
      label={$_("Comment on negotiation status")}
    />
  </EditSubsection>

  <EditSubsection title={$_("Implementation status")}>
    <!--    <JSONCurrentDateChoiceField-->
    <!--      fieldname="implementation_status"-->
    <!--      bind:value={version.implementation_status}-->
    <!--      label={$_("Implementation status")}-->
    <!--      choices={$fieldChoices.deal.implementation_status}-->
    <!--    />-->
    <TextField
      fieldname="implementation_status_comment"
      bind:value={version.implementation_status_comment}
      label={$_("Comment on implementation status")}
    />
  </EditSubsection>

  <EditSubsection title={$_("Purchase price")}>
    <!--    <DecimalField-->
    <!--      fieldname="purchase_price"-->
    <!--      bind:value={version.purchase_price}-->
    <!--      label={$_("Purchase price")}-->
    <!--      currency={version.purchase_price_currency}-->
    <!--      perType={version.purchase_price_type}-->
    <!--    />-->
    <!--    <DecimalField-->
    <!--      fieldname="purchase_price_area"-->
    <!--      bind:value={version.purchase_price_area}-->
    <!--      label={$_("Purchase price area")}-->
    <!--      unit={$_("ha")}-->
    <!--    />-->
    <TextField
      fieldname="purchase_price_comment"
      bind:value={version.purchase_price_comment}
      label={$_("Comment on purchase price")}
    />
  </EditSubsection>

  <EditSubsection title={$_("Leasing fees")}>
    <!--    <DecimalField-->
    <!--      fieldname="annual_leasing_fee"-->
    <!--      bind:value={version.annual_leasing_fee}-->
    <!--      label={$_("Annual leasing fee")}-->
    <!--      currency={version.annual_leasing_fee_currency}-->
    <!--      perType={version.annual_leasing_fee_type}-->
    <!--    />-->
    <!--    <DecimalField-->
    <!--      fieldname="annual_leasing_fee_area"-->
    <!--      bind:value={version.annual_leasing_fee_area}-->
    <!--      label={$_("Annual leasing fee area")}-->
    <!--      unit={$_("ha")}-->
    <!--    />-->
    <TextField
      fieldname="annual_leasing_fee_comment"
      bind:value={version.annual_leasing_fee_comment}
      label={$_("Comment on leasing fee")}
    />
  </EditSubsection>
  <EditSubsection title={$_("Contract farming")}>
    <!--    <BooleanField-->
    <!--      fieldname="contract_farming"-->
    <!--      bind:value={version.contract_farming}-->
    <!--      label={$_("Contract farming")}-->
    <!--    />-->
    <!--    <BooleanField-->
    <!--      fieldname="on_the_lease_state"-->
    <!--      bind:value={version.on_the_lease_state}-->
    <!--      label={$_("On leased / purchased")}-->
    <!--    />-->
    <!--    <JSONLeaseField-->
    <!--      fieldname="on_the_lease"-->
    <!--      bind:value={version.on_the_lease}-->
    <!--      label={$_("On leased area/farmers/households")}-->
    <!--    />-->
    <!--    <BooleanField-->
    <!--      fieldname="off_the_lease_state"-->
    <!--      bind:value={version.off_the_lease_state}-->
    <!--      label={$_("Not on leased / purchased (out-grower)")}-->
    <!--    />-->
    <!--    <JSONLeaseField-->
    <!--      fieldname="off_the_lease"-->
    <!--      bind:value={version.off_the_lease}-->
    <!--      label={$_("Not on leased area/farmers/households (out-grower)")}-->
    <!--    />-->
    <TextField
      fieldname="contract_farming_comment"
      bind:value={version.contract_farming_comment}
      label={$_("Comment on contract farming")}
    />
  </EditSubsection>
</form>
