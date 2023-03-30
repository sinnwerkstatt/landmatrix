<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import type { FormField } from "$components/Fields/fields"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"

  export let value: Country | undefined
  export let model: "deal" | "investor" = "deal"
  export let disabled = false
  export let formfield: FormField

  const dispatch = createEventDispatcher()

  let showHint = false

  $: isDealTargetCountry = model === "deal" && formfield.name === "country"
  $: targetCountries = isDealTargetCountry
    ? $countries.filter(c => !c.high_income)
    : $countries

  const setValue = (country: Country | null) => {
    value = country
      ? {
          id: country.id,
          name: country.name,
          code_alpha2: country.code_alpha2,
          point_lat_min: country.point_lat_min,
          point_lat_max: country.point_lat_max,
          point_lon_min: country.point_lon_min,
          point_lon_max: country.point_lon_max,
          __typename: "Country",
        }
      : undefined

    dispatch("change", value)
  }
</script>

<div
  class="country_foreignkey_field"
  on:mouseover={() => (showHint = true)}
  on:focus={() => (showHint = true)}
  on:mouseout={() => (showHint = false)}
  on:blur={() => (showHint = false)}
>
  <CountrySelect
    {value}
    countries={targetCountries}
    name={formfield.name}
    required={isDealTargetCountry}
    {disabled}
    on:input={e => setValue(e.detail)}
  />
  {#if disabled && showHint}
    <span class="absolute text-sm text-gray-500">
      {$_("You can only change the country when no locations are defined.")}
    </span>
  {/if}
</div>
