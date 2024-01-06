<script lang="ts">
  import { _ } from "svelte-i18n"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import CurrencyField from "$components/Fields/Edit2/CurrencyField.svelte"

  export let value: number | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
  export let unit: string | undefined = undefined
  export let currency: number | null | undefined = undefined
  export let perType: "PER_HA" | "PER_AREA" | null | undefined = undefined

  const PERTYPES = { PER_HA: $_("per ha"), PER_AREA: $_("for specified area") }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <div class="flex items-center gap-4">
      <LowLevelDecimalField bind:value name={fieldname} {unit} />
      {#if currency !== undefined}
        <CurrencyField bind:value={currency} />
      {/if}
      {#if perType !== undefined}
        <select bind:value={perType} class="inpt">
          <option value={null}>----</option>
          <option value="PER_HA">{PERTYPES.PER_HA}</option>
          <option value="PER_AREA">{PERTYPES.PER_AREA}</option>
        </select>
      {/if}
    </div>
  </div>
</div>
