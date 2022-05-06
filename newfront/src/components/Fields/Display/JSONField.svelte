<script lang="ts">
  import {
    dateCurrentFormat,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";

  // folgende types möglicherweise fehlerhaft oder unvollständig
  type JSONFieldType = {
    current?: boolean;
    area?: string;
    choices?: Array<{ [key: string]: string }>;
  };

  export let formfield: FormField;
  export let value: JSONFieldType[] = [];
</script>

<div class="json_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      {dateCurrentFormat(val)}
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        ({val.area} ha)
      {/if}
    </div>
  {/each}
</div>
