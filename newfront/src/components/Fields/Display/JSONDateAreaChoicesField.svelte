<script lang="ts">
  import { date_and_current, mapChoices } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: boolean;
  export let model: string;
  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsondateareachoices_field">
  {#each vals as val}
    <div class={() => (val.current ? "font-weight-bold" : "")}>
      <span>{date_and_current(val)} </span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        (<i class="fas fa-circle-notch" />
        {val.area.toLocaleString("fr")} ha)
      {/if}
    </div>
  {/each}
</div>
