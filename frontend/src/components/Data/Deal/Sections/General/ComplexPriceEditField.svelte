<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies, fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/data"

  import CurrencySelect from "$components/Fields/Edit2/CurrencySelect.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let fields: [
    "purchase_price" | "annual_leasing_fee",
    "purchase_price_currency" | "annual_leasing_fee_currency",
    "purchase_price_type" | "annual_leasing_fee_type",
    "purchase_price_area" | "annual_leasing_fee_area",
  ]
  export let version: DealVersion2
</script>

<EditField bind:value={version[fields[0]]} fieldname={fields[0]} showLabel>
  <div class="w-1/3">
    <CurrencySelect bind:value={version[fields[1]]} />
  </div>
  <select
    bind:value={version[fields[2]]}
    class="inpt w-1/3"
    class:italic={version[fields[2]] === null}
  >
    <option class="italic" value={null}>- per -</option>
    {#each $fieldChoices.deal.ha_area as { value, label }}
      <option class="not-italic" {value}>{label}</option>
    {/each}
  </select>
</EditField>

<EditField bind:value={version[fields[3]]} fieldname={fields[3]} showLabel />

{#if version[fields[0]] && version[fields[3]]}
  <div class="mx-4 mb-6 text-lg italic text-violet-600">
    {#if !version[fields[1]]}
      {$_("Please specify a currency")}
    {:else if !version[fields[2]]}
      {$_("Please specify if the amount is per total area or per ha")}
    {:else}
      {@const curSym = version[fields[1]]
        ? $currencies.find(c => c.id === version[fields[1]])?.symbol
        : "?"}

      {#if version[fields[2]] === "PER_HA"}
        {version[fields[0]]}
        {curSym}/{$_("ha")} * {version[fields[3]]}
        {$_("ha")} = {version[fields[0]] * version[fields[3]]}
        {curSym}
      {:else}
        {version[fields[0]]}
        {curSym} / {version[fields[3]]}
        {$_("ha")} =
        {(version[fields[0]] / version[fields[3]]).toFixed(2)}
        {curSym}/{$_("ha")}
      {/if}
    {/if}
  </div>
{/if}
