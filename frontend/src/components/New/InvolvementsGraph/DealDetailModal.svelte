<script lang="ts">
  import { _ } from "svelte-i18n"

  import type {
    JSONCurrentDateAreaChoicesFieldType,
    JSONCurrentDateAreaFieldType,
    JSONCurrentDateChoiceFieldType,
  } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let deal: {
    deal_id: number
    id: number
    name: string
    country_id: number | null
    intention_of_investment: JSONCurrentDateAreaChoicesFieldType[]
    implementation_status: JSONCurrentDateChoiceFieldType[]
    negotiation_status: JSONCurrentDateChoiceFieldType[]
    intended_size: number | null
    contract_size: JSONCurrentDateAreaFieldType[]
  }

  const fields = [
    "country_id",
    "intention_of_investment",
    "negotiation_status",
    "implementation_status",
    "intended_size",
    "contract_size",
  ]
</script>

<Overlay
  closeButtonText={$_("Close")}
  gotoLink={{
    href: `/deal/${deal.deal_id}/`,
    title: $_("More details about this deal"),
  }}
  on:close
  title="{$_('Deal')} {deal.name}"
  {visible}
>
  {#each fields as fieldname}
    <DisplayField {fieldname} value={deal[fieldname]} showLabel />
  {/each}
</Overlay>
