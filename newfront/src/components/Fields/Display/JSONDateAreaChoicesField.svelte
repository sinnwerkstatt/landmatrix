<script lang="ts">
  import {
    date_and_current,
    JSONDateAreaChoicesFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte";

  export let formfield: FormField;
  export let value: JSONDateAreaChoicesFieldType[] = [];
  export let model: string;
</script>

<div class="jsondateareachoices_field">
  {#each vals as val}
    <div class:font-bold={val.current}>
      <span>{date_and_current(val)} </span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        (<CircleNotchIcon /> {val.area.toLocaleString("fr")} ha)
      {/if}
    </div>
  {/each}
</div>
