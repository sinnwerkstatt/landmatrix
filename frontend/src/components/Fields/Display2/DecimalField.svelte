<script lang="ts">
  import { currencies, fieldChoices, getFieldChoicesLabel } from "$lib/stores"
  import type { Currency, HaArea } from "$lib/types/data"

  export let value: number | null

  interface Extras {
    unit?: string
    currency?: number | null
    perType?: HaArea | null
  }
  export let extras: Extras = {}

  let xcur: Currency | undefined
  $: xcur = extras.currency
    ? $currencies.find(c => c.id === extras.currency)
    : undefined
</script>

<div class="flex items-center gap-2">
  {#if value === null}
    -
  {:else}
    {value.toLocaleString("fr").replace(",", ".")}
  {/if}
  {#if extras.unit}
    {extras.unit}
  {/if}
  {#if xcur}
    <div class="italic" title={xcur.name}>
      {xcur.symbol || xcur.name}
    </div>
  {/if}
  {#if extras.perType}
    {getFieldChoicesLabel($fieldChoices["deal"]["ha_area"])(extras.perType)}
  {/if}
</div>
