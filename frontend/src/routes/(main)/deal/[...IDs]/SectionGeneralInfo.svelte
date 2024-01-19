<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection id="land_area" obj={version}>
    <DisplayField fieldname="intended_size" showLabel value={version.intended_size} />
    <DisplayField fieldname="contract_size" showLabel value={version.contract_size} />
    <DisplayField
      fieldname="production_size"
      showLabel
      value={version.production_size}
    />
    <DisplayField
      fieldname="land_area_comment"
      showLabel
      value={version.land_area_comment}
    />
  </Subsection>

  <Subsection id="intention_of_investment" obj={version}>
    <DisplayField
      fieldname="intention_of_investment"
      showLabel
      value={version.intention_of_investment}
    />
    <DisplayField
      fieldname="intention_of_investment_comment"
      showLabel
      value={version.intention_of_investment_comment}
    />
  </Subsection>

  <Subsection id="nature_of_deal" obj={version}>
    <DisplayField fieldname="nature_of_deal" showLabel value={version.nature_of_deal} />
    <DisplayField
      fieldname="nature_of_deal_comment"
      showLabel
      value={version.nature_of_deal_comment}
    />
  </Subsection>

  <Subsection id="negotiation_status" obj={version}>
    <DisplayField
      fieldname="negotiation_status"
      showLabel
      value={version.negotiation_status}
    />
    <DisplayField
      fieldname="negotiation_status_comment"
      showLabel
      value={version.negotiation_status_comment}
    />
  </Subsection>

  <Subsection id="implementation_status" obj={version}>
    <DisplayField
      fieldname="implementation_status"
      showLabel
      value={version.implementation_status}
    />
    <DisplayField
      fieldname="implementation_status_comment"
      showLabel
      value={version.implementation_status_comment}
    />
  </Subsection>

  <Subsection id="purchase_price" obj={version}>
    <DisplayField
      extras={{
        currency: version.purchase_price_currency,
        perType: version.purchase_price_type,
      }}
      fieldname="purchase_price"
      showLabel
      value={version.purchase_price}
    />
    <DisplayField
      fieldname="purchase_price_area"
      showLabel
      value={version.purchase_price_area}
    />
    <DisplayField
      fieldname="purchase_price_comment"
      showLabel
      value={version.purchase_price_comment}
    />
  </Subsection>

  <Subsection id="leasing_fee" obj={version}>
    <DisplayField
      extras={{
        currency: version.annual_leasing_fee_currency,
        perType: version.annual_leasing_fee_type,
      }}
      fieldname="annual_leasing_fee"
      showLabel
      value={version.annual_leasing_fee}
    />
    <DisplayField
      fieldname="annual_leasing_fee_area"
      showLabel
      value={version.annual_leasing_fee_area}
    />
    <DisplayField
      fieldname="annual_leasing_fee_comment"
      showLabel
      value={version.annual_leasing_fee_comment}
    />
  </Subsection>

  <Subsection id="contract_farming" obj={version}>
    <DisplayField
      fieldname="contract_farming"
      showLabel
      value={version.contract_farming}
    />
    <DisplayField
      fieldname="on_the_lease_state"
      showLabel
      value={version.on_the_lease_state}
    />
    <DisplayField fieldname="on_the_lease" showLabel value={version.on_the_lease} />
    <DisplayField
      fieldname="off_the_lease_state"
      showLabel
      value={version.off_the_lease_state}
    />
    <DisplayField fieldname="off_the_lease" showLabel value={version.off_the_lease} />
    <DisplayField
      fieldname="contract_farming_comment"
      showLabel
      value={version.contract_farming_comment}
    />
  </Subsection>
</section>
