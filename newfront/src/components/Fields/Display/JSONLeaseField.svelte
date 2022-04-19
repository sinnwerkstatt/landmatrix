<script lang="ts">
  import {
    dateCurrentFormat,
    JSONLeaseFieldType,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte";
  import HouseholdIcon from "$components/icons/HouseholdIcon.svelte";
  import TractorIcon from "$components/icons/TractorIcon.svelte";

  export let value: JSONLeaseFieldType[] = [];
</script>

<div class="jsonlease_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
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
