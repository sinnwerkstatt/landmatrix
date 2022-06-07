<script lang="ts">
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { countries } from "$lib/stores";
  import type { Country } from "$lib/types/wagtail";

  export let value: Country;
  export let model: string;

  export let disabled = false;

  let showHint = false;

  $: targetCountries =
    model === "investor" ? $countries : $countries.filter((c) => !c.high_income);
</script>

<div
  on:mouseover={() => (showHint = true)}
  on:focus={() => (showHint = true)}
  on:mouseout={() => (showHint = false)}
  on:blur={() => (showHint = false)}
>
  <Select
    items={targetCountries}
    {value}
    on:select={(e) =>
      (value = {
        __typename: "Country",
        id: e.detail.id,
        name: e.detail.name,
        code_alpha2: e.detail.code_alpha2,
        point_lat_min: e.detail.point_lat_min,
        point_lat_max: e.detail.point_lat_max,
        point_lon_min: e.detail.point_lon_min,
        point_lon_max: e.detail.point_lon_max,
      })}
    on:change
    placeholder={$_("Country")}
    optionIdentifier="id"
    labelIdentifier="name"
    showChevron
    isDisabled={disabled}
    inputStyles="cursor: not-allowed !important;"
  />
  {#if disabled && showHint}
    <span class="absolute text-sm text-gray-500">
      {$_("You can only change the country when no locations are defined.")}
    </span>
  {/if}
</div>
