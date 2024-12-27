<script lang="ts">
  import { createLabels, currencies, fieldChoices } from "$lib/stores"
  import type { Currency, HaArea } from "$lib/types/data"

  interface Extras {
    unit?: string
    currency?: number | null
    perType?: HaArea | null
  }
  interface Props {
    value: number | null
    extras?: Extras
  }

  let { value, extras = {} }: Props = $props()

  let xcur: Currency | undefined = $derived(
    $currencies.find(c => c.id === extras.currency),
  )
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
    {createLabels($fieldChoices.deal.ha_area)[extras.perType]}
  {/if}
</div>
