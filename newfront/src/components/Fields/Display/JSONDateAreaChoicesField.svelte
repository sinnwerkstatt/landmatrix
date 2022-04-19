<script lang="ts">
  import {
    dateCurrentFormat,
    JSONDateAreaChoicesFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte";

  export let formfield: FormField;
  export let value: JSONDateAreaChoicesFieldType[] = [];
</script>

<div class="jsondateareachoices_field">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)} </span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        (<CircleNotchIcon /> {val.area.toLocaleString("fr")} ha)
      {/if}
    </div>
  {/each}
</div>
