<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"

  export let value: Country | null
  export let fieldname: string

  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let model: "deal" | "investor" = "deal"
  export let disabled = false
  export let required = false

  const dispatch = createEventDispatcher()

  let showHint = false

  $: isDealTargetCountry = model === "deal" && fieldname === "country"
  $: targetCountries = isDealTargetCountry
    ? $countries.filter(c => !c.high_income)
    : $countries

  const setValue = (country: Country | null) => {
    value = country

    dispatch("change", value)
  }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <div
      on:mouseover={() => (showHint = true)}
      on:focus={() => (showHint = true)}
      on:mouseout={() => (showHint = false)}
      on:blur={() => (showHint = false)}
      role="tooltip"
    >
      <CountrySelect
        {value}
        countries={targetCountries}
        name={fieldname}
        required={required || isDealTargetCountry}
        {disabled}
        on:input={e => setValue(e.detail)}
      />

      {#if disabled && showHint}
        <span class="absolute text-sm text-gray-500">
          {$_("You can only change the country when no locations are defined.")}
        </span>
      {/if}
    </div>
  </div>
</div>
