<script lang="ts">
  import {
    date_and_current,
    JSONFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: JSONFieldType[] = [];
</script>

<div class="json_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      {date_and_current(val)}
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        ({val.area} ha)
      {/if}
    </div>
  {/each}
</div>
