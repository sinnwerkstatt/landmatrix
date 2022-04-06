<script lang="ts">
  import {
    date_and_current,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import type { FormField } from "$components/Fields/fields";
  import CircleNotchIcon from "../../icons/CircleNotchIcon.svelte";
  import TractorIcon from "../../icons/TractorIcon.svelte";
  import HouseholdIcon from "../../icons/HouseholdIcon.svelte";

  export let formfield: FormField;
  export let value: boolean;

  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsonlease_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-bold" : "")}>
      <span>{date_and_current(val)}</span>
      {#if val.area}
        <span class="mx-2">
          <CircleNotchIcon />
          {val.area.toLocaleString("fr")} ha
        </span>
      {/if}{#if val.farmers}
        <span class="mx-2">
          <TractorIcon />
          {val.farmers.toLocaleString("fr")}
        </span>
      {/if}
      {#if val.households}
        <span class="mx-2">
          <HouseholdIcon />
          {val.households.toLocaleString("fr")}
        </span>
      {/if}
    </div>
  {/each}
</div>
