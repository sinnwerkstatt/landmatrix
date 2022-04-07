<script lang="ts">
  import {
    date_and_current,
    JSONDateChoiceFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;

  export let value: JSONDateChoiceFieldType[] = [];
</script>

<div class="jsondatechoice_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{date_and_current(val)}</span>
      {#if val.choice}
        {mapChoices(val.choice, formfield.choices)}
      {/if}
    </div>
  {/each}
</div>
