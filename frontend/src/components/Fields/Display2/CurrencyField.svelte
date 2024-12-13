<script lang="ts">
  import { currencies } from "$lib/stores"
  import type { Currency } from "$lib/types/data"

  export let value: number | null

  let currency: Currency | undefined
  $: currency = $currencies.find(c => c.id === value)
</script>

{#if currency}
  <span>
    {currency.name} ({currency.symbol})
  </span>
{:else}
  <span class="italic text-red-400">
    {value}
  </span>
{/if}
