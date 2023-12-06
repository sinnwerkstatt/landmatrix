<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import JSONDateAreaChoicesField from "$components/Fields/Display2/JSONCurrentDateAreaChoicesField.svelte"
  import JSONCurrentDateAreaField from "$components/Fields/Display2/JSONCurrentDateAreaField.svelte"
  import JSONCurrentDateChoiceField from "$components/Fields/Display2/JSONCurrentDateChoiceField.svelte"
  import JSONLeaseField from "$components/Fields/Display2/JSONLeaseField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Land area")}
    fields={[
      version.intended_size,
      version.contract_size,
      version.production_size,
      version.land_area_comment,
    ]}
  >
    <DecimalField
      fieldname="intended_size"
      unit={$_("ha")}
      value={version.intended_size}
      label={$_("Intended size")}
    />
    <JSONCurrentDateAreaField
      fieldname="contract_size"
      value={version.contract_size}
      label={$_("Size under contract (leased or purchased area)")}
    />
    <JSONCurrentDateAreaField
      fieldname="production_size"
      value={version.production_size}
      label={$_("Size in operation (production)")}
    />
    <TextField
      fieldname="land_area_comment"
      value={version.land_area_comment}
      label={$_("Comment on land area")}
    />
  </Subsection>
  <Subsection
    title={$_("Intention of investment")}
    fields={[version.intention_of_investment, version.intention_of_investment_comment]}
  >
    <JSONDateAreaChoicesField
      fieldname="intention_of_investment"
      value={version.intention_of_investment}
      label={$_("Intention of investment")}
      choices={$fieldChoices.deal.intention_of_investment}
    />
    <TextField
      fieldname="intention_of_investment_comment"
      value={version.intention_of_investment_comment}
      label={$_("Comment on intention of investment")}
    />
  </Subsection>

  <Subsection
    title={$_("Nature of the deal")}
    fields={[version.nature_of_deal, version.nature_of_deal_comment]}
  >
    <TextField
      fieldname="nature_of_deal"
      value={version.nature_of_deal}
      label={$_("Nature of the deal")}
      choices={$fieldChoices.deal.nature_of_deal}
      multipleChoices
    />
    <TextField
      fieldname="nature_of_deal_comment"
      value={version.nature_of_deal_comment}
      label={$_("Comment on nature of the deal")}
    />
  </Subsection>

  <Subsection
    title={$_("Negotiation status")}
    fields={[version.negotiation_status, version.negotiation_status_comment]}
  >
    <JSONCurrentDateChoiceField
      fieldname="negotiation_status"
      value={version.negotiation_status}
      label={$_("Negotiation status")}
      choices={$fieldChoices.deal.negotiation_status}
    />
    <TextField
      fieldname="negotiation_status_comment"
      value={version.negotiation_status_comment}
      label={$_("Comment on negotiation status")}
    />
  </Subsection>

  <Subsection
    title={$_("Implementation status")}
    fields={[version.implementation_status, version.implementation_status_comment]}
  >
    <JSONCurrentDateChoiceField
      fieldname="implementation_status"
      value={version.implementation_status}
      label={$_("Implementation status")}
      choices={$fieldChoices.deal.implementation_status}
    />
    <TextField
      fieldname="implementation_status_comment"
      value={version.implementation_status_comment}
      label={$_("Comment on implementation status")}
    />
  </Subsection>

  <Subsection
    title={$_("Purchase price")}
    fields={[
      version.purchase_price,
      version.purchase_price_area,
      version.purchase_price_comment,
    ]}
  >
    <DecimalField
      fieldname="purchase_price"
      value={version.purchase_price}
      label={$_("Purchase price")}
      currency={version.purchase_price_currency}
      perType={version.purchase_price_type}
    />
    <DecimalField
      fieldname="purchase_price_area"
      value={version.purchase_price_area}
      label={$_("Purchase price area")}
      unit={$_("ha")}
    />
    <TextField
      fieldname="purchase_price_comment"
      value={version.purchase_price_comment}
      label={$_("Comment on purchase price")}
    />
  </Subsection>

  <Subsection
    title={$_("Leasing fees")}
    fields={[
      version.annual_leasing_fee,
      version.annual_leasing_fee_area,
      version.annual_leasing_fee_comment,
    ]}
  >
    <DecimalField
      fieldname="annual_leasing_fee"
      value={version.annual_leasing_fee}
      label={$_("Annual leasing fee")}
      currency={version.annual_leasing_fee_currency}
      perType={version.annual_leasing_fee_type}
    />
    <DecimalField
      fieldname="annual_leasing_fee_area"
      value={version.annual_leasing_fee_area}
      label={$_("Annual leasing fee area")}
      unit={$_("ha")}
    />
    <TextField
      fieldname="annual_leasing_fee_comment"
      value={version.annual_leasing_fee_comment}
      label={$_("Comment on leasing fee")}
    />
  </Subsection>
  <Subsection
    title={$_("Contract farming")}
    fields={[
      version.contract_farming,
      version.on_the_lease_state,
      version.on_the_lease,
      version.off_the_lease_state,
      version.off_the_lease,
      version.contract_farming_comment,
    ]}
  >
    <BooleanField
      fieldname="contract_farming"
      value={version.contract_farming}
      label={$_("Contract farming")}
    />
    <BooleanField
      fieldname="on_the_lease_state"
      value={version.on_the_lease_state}
      label={$_("On leased / purchased")}
    />
    <JSONLeaseField
      fieldname="on_the_lease"
      value={version.on_the_lease}
      label={$_("On leased area/farmers/households")}
    />
    <BooleanField
      fieldname="off_the_lease_state"
      value={version.off_the_lease_state}
      label={$_("Not on leased / purchased (out-grower)")}
    />
    <JSONLeaseField
      fieldname="off_the_lease"
      value={version.off_the_lease}
      label={$_("Not on leased area/farmers/households (out-grower)")}
    />
    <TextField
      fieldname="contract_farming_comment"
      value={version.contract_farming_comment}
      label={$_("Comment on contract farming")}
    />
  </Subsection>
</section>
