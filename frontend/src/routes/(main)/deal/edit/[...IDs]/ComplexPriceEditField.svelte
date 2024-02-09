<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import EditField from "$components/Fields/EditField.svelte"
  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  export let fields: [
    "purchase_price" | "annual_leasing_fee",
    "purchase_price_currency" | "annual_leasing_fee_currency",
    "purchase_price_type" | "annual_leasing_fee_type",
    "purchase_price_area" | "annual_leasing_fee_area",
  ]
  export let version: DealVersion2

  const PERTYPES = { PER_HA: $_("per ha"), PER_AREA: $_("for specified area") }
</script>

<EditField bind:value={version[fields[0]]} fieldname={fields[0]} showLabel>
  <div class="w-1/3">
    {#if $currencies}
      <VirtualListSelect
        value={$currencies.find(c => c.id === version[fields[1]])}
        items={$currencies}
        placeholder={$_("Currency")}
        label="name"
        on:input={e => (version[fields[1]] = e?.detail?.id ?? null)}
      >
        <svelte:fragment slot="selection" let:selection>
          {selection.name} ({selection.code})
        </svelte:fragment>
        <svelte:fragment slot="item" let:item>
          {item.name} ({item.code})
        </svelte:fragment>
      </VirtualListSelect>
    {/if}
  </div>
  <select
    bind:value={version[fields[2]]}
    class="inpt w-1/3"
    class:italic={version[fields[2]] === null}
  >
    <option class="italic" value={null}>- per -</option>
    <option class="not-italic" value="PER_HA">{PERTYPES.PER_HA}</option>
    <option class="not-italic" value="PER_AREA">{PERTYPES.PER_AREA}</option>
  </select>
</EditField>
<EditField bind:value={version[fields[3]]} fieldname={version[fields[3]]} showLabel />
{#if version[fields[0]] && version[fields[3]]}
  <div class="mx-4 mb-6 text-lg italic text-violet-600">
    {#if !version[fields[1]]}
      Please specify a currency
    {:else if !version[fields[2]]}
      Please specify if the amount is per total area or per ha
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
