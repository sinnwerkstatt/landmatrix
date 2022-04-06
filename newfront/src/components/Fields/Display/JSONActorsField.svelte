<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { mapChoices } from "$components/Fields/Display/jsonHelpers";

  export let formfield: FormField;
  export let value: boolean;
  export let model: string;
  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsonactors_field whitespace-nowrap">
  {#each vals as val}
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
