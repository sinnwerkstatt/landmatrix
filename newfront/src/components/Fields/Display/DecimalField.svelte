<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: number;
  export let model: string;
</script>

<div class="decimal_field whitespace-nowrap">
  {formfield?.choices ? formfield.choices[value] : value.toLocaleString("fr")}
  {#if formfield.unit}
    <span>{formfield.unit}</span>
  {/if}
</div>
