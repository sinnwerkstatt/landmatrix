<script lang="ts">
  import {
    date_and_current,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import CircleNotchIcon from "../../icons/CircleNotchIcon.svelte";
  import WeightIcon from "../../icons/WeightIcon.svelte";
  import type { FormField } from "$components/Fields/fields";
  import PlaneIcon from "../../icons/PlaneIcon.svelte";

  export let value: boolean;
  export let formfield: FormField;
  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsonexports_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-bold" : "")}>
      <span>{date_and_current(val)}</span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}{#if val.area}
        <span> <CircleNotchIcon /> {val.area.toLocaleString("fr")} ha</span>
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
