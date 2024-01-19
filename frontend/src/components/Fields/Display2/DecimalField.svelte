<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies } from "$lib/stores"
  import type { Currency } from "$lib/types/newtypes"

  export let value: number | null

  interface Extras {
    unit?: string
    currency?: number | null
    perType?: "PER_HA" | "PER_AREA" | null
  }
  export let extras: Extras = {}

  let xcur: Currency | undefined
  $: xcur = extras.currency
    ? $currencies.find(c => c.id === extras.currency)
    : undefined

  const PERTYPES = { PER_HA: $_("per ha"), PER_AREA: $_("for specified area") }
</script>

<div class="flex items-center gap-2">
  {value?.toLocaleString("fr") ?? "—"}
  {#if extras.unit}
    {extras.unit}
  {/if}
  {#if xcur}
    <div class="italic" title={xcur.name}>
      {xcur.symbol || xcur.name}
    </div>
  {/if}
  {#if extras.perType}
    {PERTYPES[extras.perType]}
  {/if}
</div>
