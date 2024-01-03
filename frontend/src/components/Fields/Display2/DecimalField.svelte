<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies } from "$lib/stores"
  import type { Currency } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: number | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
  export let unit: string | undefined = undefined
  export let currency: number | null | undefined = undefined

  export let perType: "PER_HA" | "PER_AREA" | null | undefined = undefined

  let xcur: Currency | undefined
  $: xcur = currency ? $currencies.find(c => c.id === currency) : undefined

  const PERTYPES = { PER_HA: $_("per ha"), PER_AREA: $_("for specified area") }
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <div class="flex items-center gap-2">
        {value?.toLocaleString("fr") ?? "—"}
        {#if value && unit}
          {unit}
        {/if}
        {#if value && xcur}
          <div class="italic" title={xcur.name}>
            {xcur.symbol || xcur.name}
          </div>
        {/if}
        {#if value && perType}
          {PERTYPES[perType]}
        {/if}
      </div>
    </div>
  </div>
{/if}
