<script lang="ts">
  import {
    date_and_current,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers.ts";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: boolean;

  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="json_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-bold" : "")}>
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
