<script lang="ts">
  import {
    JSONActorsFieldType,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: JSONActorsFieldType[] = [];
  export let model: string;
</script>

<div class="jsonactors_field whitespace-nowrap">
  {#each value as val}
    <div>
      <span>{val.name}</span>
      {#if val.role}
        <span class="font-weight-light">
          ({mapChoices(val.role, formfield.choices)})
        </span>
      {/if}
    </div>
  {/each}
</div>
