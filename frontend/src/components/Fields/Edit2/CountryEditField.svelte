<script lang="ts">
  import Select from "svelte-select"

  import { page } from "$app/state"

  interface Props {
    value: number | null
    extras?: { required?: boolean; excludeHighIncome?: boolean }
  }

  let {
    value = $bindable(),
    extras = { required: false, excludeHighIncome: false },
  }: Props = $props()

  let targetCountries = $derived(
    extras.excludeHighIncome
      ? page.data.countries.filter(c => !c.high_income)
      : page.data.countries,
  )
</script>

<Select
  itemId="id"
  items={targetCountries}
  label="name"
  on:change={e => (value = e.detail.id)}
  on:clear={() => (value = null)}
  required={extras.required}
  value={targetCountries.find(c => c.id === value)}
/>
