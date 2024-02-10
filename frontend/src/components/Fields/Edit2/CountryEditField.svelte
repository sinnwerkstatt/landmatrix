<script lang="ts">
  import Select from "svelte-select"

  import { countries } from "$lib/stores"

  export let value: number | null
  export let fieldname: string

  export let extras = { required: false }
  export let model: "deal" | "investor" = "deal"

  $: isDealTargetCountry = model === "deal" && fieldname === "country"
  $: targetCountries = isDealTargetCountry
    ? $countries.filter(c => !c.high_income)
    : $countries
</script>

<Select
  itemId="id"
  items={targetCountries}
  label="name"
  on:change={e => (value = e.detail.id)}
  required={extras.required}
  value={targetCountries.find(c => c.id === value)}
/>
