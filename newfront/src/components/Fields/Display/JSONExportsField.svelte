<script lang="ts">
  import {
    dateCurrentFormat,
    JSONExportsFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import type { FormField } from "$components/Fields/fields";
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte";
  import PlaneIcon from "$components/icons/PlaneIcon.svelte";
  import WeightIcon from "$components/icons/WeightIcon.svelte";

  export let value: JSONExportsFieldType[] = [];
  export let formfield: FormField;
</script>

<div class="jsonexports_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}{#if val.area}
        <span>
          <CircleNotchIcon />
          {val.area.toLocaleString("fr")} ha
        </span>
      {/if}{#if val.yield}
        <span class="mx-2">
          <WeightIcon />
          {val.yield.toLocaleString("fr")} tons
        </span>
      {/if}{#if val.export}
        <span class="mx-2">
          <PlaneIcon />
          {val.export.toLocaleString("fr")} %
        </span>
      {/if}
    </div>
  {/each}
</div>
