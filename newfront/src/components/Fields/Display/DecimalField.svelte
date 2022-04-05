<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: number;
  export let model: string;

  $: val = formfield?.choices ? formfield.choices[value] : value.toLocaleString("fr");
</script>

<div class="decimal_field whitespace-nowrap">
  {val}
  {#if formfield.unit}
    <span>{formfield.unit}</span>
  {/if}
</div>
