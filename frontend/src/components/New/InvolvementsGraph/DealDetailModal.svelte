<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Deal } from "$lib/types/deal"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let deal: Deal

  const fields = [
    "country",
    "intention_of_investment",
    "implementation_status",
    "negotiation_status",
    "intended_size",
    "contract_size",
  ]
  const createTitle = (deal: Deal) => `${deal.name}`
</script>

<Overlay on:close title={createTitle(deal)} {visible}>
  <div>
    <CountryField
      fieldname="deal.country"
      label={$_("Target country")}
      value={deal.country_id}
    />
    <!--{#each fields as fieldName}-->
    <!--  <DisplayField-->
    <!--    fieldname={fieldName}-->
    <!--    value={deal[fieldName]}-->
    <!--    model="deal"-->
    <!--    showLabel-->
    <!--  />-->
    <!--{/each}-->
    <div class="w-100 mt-8">
      <a class="deal" href="/deal/{deal._id}" rel="noreferrer" target="_blank">
        {$_("More details about this deal")}
      </a>
    </div>
  </div>
</Overlay>
