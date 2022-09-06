<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import type { FormField } from "$components/Fields/fields"

  export let value: Country | undefined
  export let model: string
  export let disabled = false
  export let formfield: FormField

  const dispatch = createEventDispatcher()

  let showHint = false

  $: targetCountries =
    model === "investor" ? $countries : $countries.filter(c => !c.high_income)

  const onSelect = e => {
    value = e?.detail
      ? {
          __typename: "Country",
          id: e.detail.id,
          name: e.detail.name,
          code_alpha2: e.detail.code_alpha2,
          point_lat_min: e.detail.point_lat_min,
          point_lat_max: e.detail.point_lat_max,
          point_lon_min: e.detail.point_lon_min,
          point_lon_max: e.detail.point_lon_max,
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
  <Select
    items={targetCountries}
    {value}
    on:select={onSelect}
    on:clear={onSelect}
    placeholder={$_("Country")}
    optionIdentifier="id"
    labelIdentifier="name"
    showChevron
    isDisabled={disabled}
    inputAttributes={{ name: formfield.name }}
  />
  {#if disabled && showHint}
    <span class="absolute text-sm text-gray-500">
      {$_("You can only change the country when no locations are defined.")}
    </span>
  {/if}
</div>
