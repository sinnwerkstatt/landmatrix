<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import Select from "svelte-select"

  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"

  export let value: number | null
  export let fieldname: string

  export let extras = { required: false }
  export let model: "deal" | "investor" = "deal"

  const dispatch = createEventDispatcher()

  $: isDealTargetCountry = model === "deal" && fieldname === "country"
  $: targetCountries = isDealTargetCountry
    ? $countries.filter(c => !c.high_income)
    : $countries

  // const setValue = (country: Country | null) => {
  //   value = country
  //
  //   dispatch("change", value)
  // }
</script>

<Select
  items={targetCountries}
  value={targetCountries.find(c => c.id === value)}
  on:change={e => (value = e.detail.id)}
  label="name"
  itemId="id"
  required={extras.required}
/>
<!--  <CountrySelect-->
<!--    countries={targetCountries}-->
<!--    name={fieldname}-->
<!--    on:input={e => setValue(e.detail)}-->
<!--    required={required || isDealTargetCountry}-->
<!--    {value}-->
<!--  />-->
